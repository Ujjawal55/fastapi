from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from fastapi import FastAPI

app = FastAPI()


class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str
    description: Optional[str] = Field(
        title="Description of the book",
        min_length=1,
        max_length=100,
    )
    rating: int = Field(ge=1, le=100)

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "60c3c928-f9ed-47da-9341-cdb5339c6f9f",
                "title": "hello, world",
                "author": "programming world",
                "description": "first word for any programmer",
                "rating": 100,
            }
        }
    }


# list of data book: Book(type)
BOOKS = []


@app.get("/")
async def get_all_books(books_to_return: Optional[int] = None):
    if len(BOOKS) < 1:
        create_book_no_api()
    if books_to_return is not None:
        if books_to_return < 0:
            return "books_to_return should be >= 0"
        if books_to_return <= len(BOOKS) > 0:
            return BOOKS[:books_to_return]
    return BOOKS


@app.post("/")
async def create_book(book: Book):
    BOOKS.append(book)
    return BOOKS


@app.put("/{book_id}")
async def update_books(book_id: UUID, book: Book):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS[i] = book
            return BOOKS[i]
    return f"No books exist with id {book_id}"


@app.delete("/{book_id}")
async def delete_book(book_id: UUID):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            del BOOKS[i]
            return BOOKS
    return f"No book exist with id {book_id}"


@app.get("/books/{book_id}")
async def read_book(book_id: UUID):
    for book in BOOKS:
        if book.id == book_id:
            return book

    return f"No book exist with id {book_id}"


def create_book_no_api():
    book1 = Book(
        id="6023c928-f9ed-47da-9341-cdb5339c6f9f",  # type: ignore
        title="title1",
        author="author1",
        description="description 1",
        rating=60,
    )

    book2 = Book(
        id="7023c928-f9ed-47da-9341-cdb5339c6f9f",  # type: ignore
        title="title2",
        author="author2",
        description="description 2",
        rating=60,
    )

    book3 = Book(
        id="8023c928-f9ed-47da-9341-cdb5339c6f9f",  # type: ignore
        title="title3",
        author="author3",
        description="description 3",
        rating=60,
    )

    BOOKS.append(book1)
    BOOKS.append(book2)
    BOOKS.append(book3)
