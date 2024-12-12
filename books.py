from enum import Enum
from typing import Optional

from fastapi import FastAPI

app = FastAPI()

BOOKS = {
    "book_1": {"name": "Book One", "author": "Author One"},
    "book_2": {"name": "Book Two", "author": "Author Two"},
    "book_3": {"name": "Book Three", "author": "Author Three"},
}


# enumeration in the path parameter
class DirectionName(str, Enum):
    east = "East"
    west = "west"
    north = "North"
    south = "South"


# @app.get("/")
# async def get_all_books():
#     return BOOKS


@app.get("/")
async def get_books(skip_book: Optional[str] = None):

    if skip_book:
        new_book = BOOKS.copy()
        del new_book[skip_book]
        return new_book

    return BOOKS


@app.get("/direction/{direction_name}")
async def get_direction(direction_name: DirectionName):
    if direction_name == DirectionName.north:
        return ({"Direction": direction_name, "sub": "Up"},)
    if direction_name == DirectionName.east:
        return ({"Direction": direction_name, "sub": "right"},)
    if direction_name == DirectionName.south:
        return ({"Direction": direction_name, "sub": "Down"},)
    if direction_name == DirectionName.west:
        return ({"Direction": direction_name, "sub": "Left"},)


@app.get("/books/{book_name}")
async def read_book(book_name: str):
    book_detail = BOOKS.get(book_name)
    if book_detail is not None:
        return book_detail
    return "No book found"


@app.post("/")
async def create_book(book_title: str, author: str):
    # case1: the BOOkS is empty

    value = {
        "book_title": book_title,
        "author": author,
    }

    key = ""

    if len(BOOKS) == 0:
        key = "book_1"

    else:
        try:
            last_book_name = list(BOOKS.keys())[-1]
            last_key_number = last_book_name.split("_")[-1]

            current_key_number = int(last_key_number) + 1

            key = "book_" + str(current_key_number)
        except ValueError:
            raise ValueError("Internally parsing failed")

    BOOKS[key] = value
    return BOOKS


@app.put("/{book_name}")
async def update_book(book_name: str, title: str, author: str):

    book_description = {
        "book_title": title,
        "author_name": author,
    }

    if book_name in BOOKS:
        BOOKS[book_name] = book_description
        return BOOKS

    return "No books exist"


@app.delete("/{book_name}")
async def delete_book(book_name: str):
    if book_name in BOOKS:
        del BOOKS[book_name]
        return f"{book_name} is deleted"
    return f"{book_name} does not exist"
