from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field
from starlette.responses import JSONResponse

from fastapi import FastAPI, HTTPException, Request


class NegativeNumberException(Exception):
    def __init__(self, books_to_return: int):
        self.books_to_return = books_to_return


app = FastAPI()


@app.exception_handler(Exception)
async def negative_number_exception_handler(
    request: Request, exception: NegativeNumberException
):
    return JSONResponse(
        status_code=418,
        content={
            "message": f"hey, why do you need {exception.books_to_return}\nyou should read more books."
        },
    )


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


class BookNoRating(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str
    description: Optional[str] = Field(
        None,
        title="Description of the book",
        min_length=1,
        max_length=100,
    )


# list of data book: Book(type)
BOOKS = []


@app.get("/")
async def get_all_books(books_to_return: Optional[int] = None):
    if books_to_return and books_to_return < 0:
        raise NegativeNumberException(books_to_return)
    if len(BOOKS) < 1:
        create_book_no_api()
    if books_to_return is not None:
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
    raise not_found_404()


@app.delete("/{book_id}")
async def delete_book(book_id: UUID):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            del BOOKS[i]
            return BOOKS
    raise not_found_404()


@app.get("/books/{book_id}")
async def read_book(book_id: UUID):
    for book in BOOKS:
        if book.id == book_id:
            return book

    raise not_found_404()


@app.get("/books/rating/{book_id}", response_model=BookNoRating)
async def read_book_no_rating(book_id: UUID):
    for book in BOOKS:
        if book.id == book_id:
            return book

    raise not_found_404()


def create_book_no_api():
    book1 = Book(
        id="6023c928-f9ed-47da-9341-cdb5339c6f9f",  # type: ignore
        title="Title 1",
        author="Author 1",
        description="Description 1",
        rating=60,
    )

    book2 = Book(
        id="7023c928-f9ed-47da-9341-cdb5339c6f9f",  # type: ignore
        title="Title 2",
        author="Author 2",
        description="Description 2",
        rating=60,
    )

    book3 = Book(
        id="8023c928-f9ed-47da-9341-cdb5339c6f9f",  # type: ignore
        title="Title 3",
        author="Author 3",
        description="Description 3",
        rating=60,
    )

    BOOKS.append(book1)
    BOOKS.append(book2)
    BOOKS.append(book3)


def not_found_404():
    return HTTPException(status_code=404, detail="Book not found")
