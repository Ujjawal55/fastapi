from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

import models
from database import SessionLocal, engine

SECERT_KEY = "put_hash_value_in_here"
ALGORITHM = "HS256"


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")


class UserCreate(BaseModel):

    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    hashed_password: str


app = FastAPI()


models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def verify_hashed_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)


def is_user_exist(username: str, password: str, db) -> bool:
    user = db.query(models.Users).filter(models.Users.username == username).first()

    if not user:
        return False
    if not verify_hashed_password(password, user.hashed_password):
        return False
    return user


def create_access_token(
    username: str, user_id: int, expire_delta: Optional[timedelta] = None
):
    encode = {"sub": username, "id": user_id}

    if expire_delta:
        expire = datetime.utcnow() + expire_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    encode.update({"exp": expire})

    return jwt.encode(encode, SECERT_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECERT_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub", None)
        user_id = payload.get("id", None)
        if username is None or user_id is None:
            raise HTTPException(status_code=404, detail="User not found")
        return {
            "username": username,
            "user_id": user_id,
        }

    except JWTError:
        raise HTTPException(status_code=404, detail="User not found")


@app.post("/create/user")
async def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    user_model = models.Users(
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=get_hashed_password(user.hashed_password),
        is_active=True,
    )

    db.add(user_model)
    db.commit()

    return {"status": 200, "message": "User has been created."}


@app.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = is_user_exist(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    token_expires = timedelta(minutes=15)
    token = create_access_token(user.username, user.id, expire_delta=token_expires)

    return {"token": token}


def get_hashed_password(password):
    return bcrypt_context.hash(password)
