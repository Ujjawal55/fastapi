from fastapi import Depends, FastAPI, HTTPException
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


@app.get("/")
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.Todo).all()


@app.get("/todo/{todo_id}")
async def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()

    if todo is not None:
        return todo
    raise http_exception_404()


def http_exception_404():
    return HTTPException(status_code=404, detail="Todo does not exist.")
