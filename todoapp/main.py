from typing import Optional

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

import models
from database import SessionLocal, engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# pydjantic model for the post request::


class TodoCreate(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(
        ge=1, le=5, description="priority should be in between 1 and 5"
    )
    complete: bool


@app.get("/")
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.Todo).all()


# post request to create the todo
@app.post("/")
async def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = models.Todo(
        title=todo.title,
        description=todo.description,
        priority=todo.priority,
        complete=todo.complete,
    )

    db.add(db_todo)
    db.commit()

    return {"status_code": 201, "message": "record has been successfully created"}


@app.get("/todo/{todo_id}")
async def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()

    if todo is not None:
        return todo
    raise http_exception_404()


# put request to the todo
@app.put("/{todo_id}")
async def update_todo(todo_id: int, todo: TodoCreate, db: Session = Depends(get_db)):
    # get the particular instance of the data
    todo_model = db.query(models.Todo).filter(models.Todo.id == todo_id).first()

    if todo_model is None:
        raise http_exception_404()

    todo_model.title = todo.title  # type: ignore
    todo_model.description = todo.description  # type: ignore
    todo_model.priority = todo.priority  # type: ignore
    todo_model.complete = todo.complete  # type: ignore

    db.add(todo_model)
    db.commit()

    return http_status_code_200()


# delete request
@app.delete("/{todo_id}")
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo_model = db.query(models.Todo).filter(models.Todo.id == todo_id).first()

    if todo_model is None:
        raise http_exception_404()

    db.delete(todo_model)
    db.commit()
    return http_status_code_200()


def http_status_code_200():
    return {"status": 200, "message": "successfull"}


def http_exception_404():
    return HTTPException(status_code=404, detail="Todo does not exist.")
