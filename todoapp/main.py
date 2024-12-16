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


def http_exception_404():
    return HTTPException(status_code=404, detail="Todo does not exist.")
