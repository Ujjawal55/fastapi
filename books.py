from enum import Enum

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


@app.get("/")
async def get_all_books():
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
