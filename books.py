from fastapi import FastAPI

app = FastAPI()

BOOKS = {
    "book_1": {"name": "Book One", "author": "Author One"},
    "book_2": {"name": "Book Two", "author": "Author Two"},
    "book_3": {"name": "Book Three", "author": "Author Three"},
}


@app.get("/")
async def get_all_books():
    return BOOKS
