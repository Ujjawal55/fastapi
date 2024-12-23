from typing import Optional

from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import SessionLocal
from fastapi import APIRouter, Depends, HTTPException
from models import Address, Users
from routers.auth import get_current_user


class AddressCreate(BaseModel):
    address1: str
    address2: Optional[str]
    city: str
    state: str
    country: str
    postalcode: str


router = APIRouter(
    prefix="/address", tags=["address"], responses={404: {"description": "Not Found"}}
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close_all()


@router.get("/")
async def get_address(
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    user = db.query(Users).filter(Users.id == user.get("user_id")).first()

    if user:
        return user.user_address
    return None


@router.post("/")
async def create_address(
    address: AddressCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    user_model = db.query(Users).filter(Users.id == user.get("user_id")).first()

    if not user_model:
        raise HTTPException(status_code=404, detail="User not found")

    address_model = Address(
        address1=address.address1,
        address2=address.address2,
        city=address.city,
        state=address.state,
        country=address.country,
        postalcode=address.postalcode,
    )
    db.add(address_model)
    db.commit()
    db.refresh(address_model)

    user_model.address_id = address_model.id
    db.add(user_model)
    db.commit()
    db.refresh(user_model)

    return user_model.user_address


@router.put("/{address_id}")
async def update_address(
    address_id: int,
    address: AddressCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    user = db.query(Users).filter(Users.id == user.get("user_id")).first()

    if user is None or user.user_address.id != address_id:
        raise HTTPException(
            status_code=404,
            detail={"message": "Address not found or doesn't belong to user"},
        )
    address_model = user.user_address
    if address_model is None:
        return HTTPException(
            status_code=404, detail={"message": "address does not exist"}
        )
    address_model.address1 = address.address1
    address_model.address2 = address.address2
    address_model.city = address.city
    address_model.state = address.state
    address_model.country = address.country
    address_model.postalcode = address.postalcode
    db.add(address_model)
    db.commit()

    return user.user_address


@router.delete("/{address_id}")
async def delete_address(
    address_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):

    user = db.query(Users).filter(Users.id == user.get("user_id")).first()

    if user is None or user.user_address.id != address_id:
        raise HTTPException(
            status_code=404,
            detail={"message": "Address not found or doesn't belong to user"},
        )
    address_model = user.user_address
    db.delete(address_model)
    db.commit()
    return {200: {"description": "address successfully deleted"}}
