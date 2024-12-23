from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import SessionLocal
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models import Users

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
    phone_number: str


router = APIRouter(
    prefix="/auth", tags=["auth"], responses={401: {"user": "Not authorized"}}
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def verify_hashed_password(plain_password, hashed_password):
    print(f"hashed_password: {hashed_password}")
    return bcrypt_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str, db) -> bool:
    user = db.query(Users).filter(Users.username == username).first()

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
            raise HTTPException(status_code=401, detail="Unauthorized")
        return {
            "username": username,
            "user_id": user_id,
        }

    except JWTError:
        raise HTTPException(status_code=401, detail="User not found")


@router.post("/create/user")
async def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    user_model = Users(
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=get_hashed_password(user.hashed_password),
        is_active=True,
        phone_number=user.phone_number,
    )

    db.add(user_model)
    db.commit()

    return {"status": 200, "message": "User has been created."}


@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    token_expires = timedelta(minutes=15)
    token = create_access_token(user.username, user.id, expire_delta=token_expires)  # type: ignore

    return {"token": token}


def get_hashed_password(password):
    return bcrypt_context.hash(password)
