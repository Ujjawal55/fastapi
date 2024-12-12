from uuid import UUID

from pydantic import BaseModel

from fastapi import FastAPI

app = FastAPI()


class Book(BaseModel):
    id: UUID
    title: str
    author: str
    description: str
    rating: int


BOOKS = []


@app.get("/")
async def get_all_books():
    return BOOKS
