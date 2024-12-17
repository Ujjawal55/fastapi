from typing import Optional

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy import FallbackAsyncAdaptedQueuePool
from sqlalchemy.orm import Session

import models
from database import SessionLocal, engine

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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

    return "user validated"


def get_hashed_password(password):
    return bcrypt_context.hash(password)
