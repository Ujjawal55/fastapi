from typing import Optional

import models
from database import SessionLocal
from pydantic import BaseModel, Field
from routers.auth import get_current_user
from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(
    prefix="/todos", tags=["todos"], responses={404: {"description": "not found"}}
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# NOTE: pydjantic model for the post request::


class TodoCreate(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(
        ge=1, le=5, description="priority should be in between 1 and 5"
    )
    complete: bool


@router.get("/")
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.Todo).all()


# NOTE:  post request to create the todo
@router.post("/")
async def create_todo(
    todo: TodoCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):

    if user is None:
        raise http_exception_404()

    db_todo = models.Todo(
        title=todo.title,
        description=todo.description,
        priority=todo.priority,
        complete=todo.complete,
        owner_id=user.get("user_id"),
    )

    db.add(db_todo)
    db.commit()

    return {"status_code": 201, "message": "record has been successfully created"}


# NOTE: get request to get the todo using todo_id
@router.get("/{todo_id}")
async def read_todo(
    todo_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)
):
    if user is None:
        raise http_exception_404()

    todo = (
        db.query(models.Todo)
        .filter(models.Todo.id == todo_id)
        .filter(models.Todo.owner_id == user.get("user_id"))
        .first()
    )
    if todo is not None:
        return todo
    raise http_exception_404()


# NOTE: put request to the todo
@router.put("/{todo_id}")
async def update_todo(
    todo_id: int,
    todo: TodoCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):

    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    # get the particular instance of the data
    todo_model = (
        db.query(models.Todo)
        .filter(models.Todo.id == todo_id)
        .filter(models.Todo.owner_id == user.get("user_id"))
        .first()
    )

    if todo_model is None:
        raise http_exception_404()

    todo_model.title = todo.title  # type: ignore
    todo_model.description = todo.description  # type: ignore
    todo_model.priority = todo.priority  # type: ignore
    todo_model.complete = todo.complete  # type: ignore
    todo_model.owner_id = user.get("user_id")  # type: ignore

    db.add(todo_model)
    db.commit()

    return http_status_code_200()


# NOTE:  delete request


@router.delete("/{todo_id}")
async def delete_todo(
    todo_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)
):

    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    todo_model = (
        db.query(models.Todo)
        .filter(models.Todo.id == todo_id)
        .filter(models.Todo.owner_id == user.get("user_id"))
        .first()
    )

    if todo_model is None:
        raise http_exception_404()

    db.delete(todo_model)
    db.commit()
    return http_status_code_200()


def http_status_code_200():
    return {"status": 200, "message": "successfull"}


def http_exception_404():
    return HTTPException(status_code=404, detail="Todo does not exist.")


# NOTE: authentication of user


@router.get("/user")
async def read_all_by_user(
    user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):

    if user is None:
        raise HTTPException(status_code=404, detail="user not found")

    return (
        db.query(models.Todo).filter(models.Todo.owner_id == user.get("user_id")).all()
    )
