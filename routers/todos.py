from typing import Optional

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

import models
from database import SessionLocal
from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from routers.auth import get_current_user

router = APIRouter(
    prefix="/todos", tags=["todos"], responses={404: {"description": "not found"}}
)

templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_class=HTMLResponse, name="todos")
async def read_all_by_user(request: Request, db: Session = Depends(get_db)):
    todos = db.query(models.Todo).filter(models.Todo.owner_id == 1).all()
    return templates.TemplateResponse(
        "home.html", context={"request": request, "todos": todos}
    )


@router.get("/add-todo", response_class=HTMLResponse, name="add-todo")
async def add_new_todo(request: Request):
    return templates.TemplateResponse("add-todo.html", context={"request": request})


@router.post("/add-todo", response_class=HTMLResponse)
async def create_todo(
    request: Request,
    title: str = Form(...),
    description: str = Form(...),
    priority: int = Form(...),
    db: Session = Depends(get_db),
):
    todo_model = models.Todo(
        title=title,
        description=description,
        priority=priority,
        complete=False,
        owner_id=1,
    )
    db.add(todo_model)
    db.commit()
    return RedirectResponse(url="/todos/", status_code=status.HTTP_302_FOUND)


@router.get("/edit-todo/{todo_id}", response_class=HTMLResponse)
async def edit_todo(request: Request):
    return templates.TemplateResponse("edit-todo.html", context={"request": request})
