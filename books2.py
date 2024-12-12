from fastapi import FastAPI

app = FastAPI()

BOOKS = []


@app.get("/")
async def get_all_books():
    return BOOKS
