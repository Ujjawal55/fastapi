# command to run the dependency

- pip install fastapi\[all\] (use the escape character because of zsh has some built-in feature for [])

---

# command to run the server

- uvicorn file_name:app --reload

---

# Route Matching in FastAPI: Why Order Matters

- In FastAPI, **order matters** when defining routes with path parameters because FastAPI processes the routes in the order they are defined in your code. - This can affect which route matches an incoming request.

## Example of Incorrect Order

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/{username}")
async def get_user(username: str):
    return {"username": username}

@app.get("/admin")
async def get_admin():
    return {"message": "Admin panel"}


```

- example: if we send request to **localhost:8000/admin**,
- the fastapi catches that **admin** as **username** and execute the **get_user()** method.

---

# Enumeration code

```python

from enum import Enum

class Role(str, Enum):
    admin = "admin"
    user = "user"
    guest = "guest"

print(Role.admin)          # Output: Role.admin
print(Role.admin.value)    # Output: admin
```

- **NOTE:** Role inherit two class str, Enum. str class make sure that member of the class is treated as String

---

# creating a pydantic class object

```python

from uuid import UUID

from pydantic import BaseModel

class Book(BaseModel):
    id: UUID
    title: str
    author: str
    description: str
    rating: int

@app.post("/")
async def create_book(book: Book):
    BOOKS.append(book)

```

**NOTE:** since the book is type Book which is a inheritence of BaseModel of the pydantic. therefore, the fastapi assume that the book data will in the body

---

# Field class from pydantic

```python

from pydantic import BaseModel, Field


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

```

---

# model_config

```python
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
```

---

# HTTPException

```python
from fastapi import FastAPI, HTTPException

def not_found_404():
  return HTTPException(status_code=404, detail="<detail in here>")

# call this function with the raise keyword.


```

---

# custom exception

```python

class NegativeNumberException(Exception):
    def __init__(self, books_to_return: int):
        self.books_to_return = books_to_return


app = FastAPI()


@app.exception_handler(Exception)
async def negative_number_exception_handler(
    request: Request, exception: NegativeNumberException
):
  """
    decorator for the custom exception

    Args:
      request(Request): contains the information about the HTTP request.
      exception(NegativeNumberException): instance of the NegativeNumberException class.

    Return:
      JSONResponse containing the custom message for the exception

  """
    return JSONResponse(
        status_code=418,
        content={
            "message": f"hey, why do you need {exception.books_to_return}\nyou should read more books."
        },
    )

```

## NOTE: use the function with the <u>raise</u> keyword.

---

# Response class

```python

from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float

app = FastAPI()

@app.get("/items/", response_model=Item)
async def read_item():
    return {"name": "Book", "price": 15.99, "secret_data": "hidden"}
# here fast api will filter out the {seceret_data}.
```

---

# Form

```python

@app.post("/book/login")
async def book_login(username: str = Form(), password: str = Form()):
    return {
        "username": username,
        "password": password,
    }

```

---

# SqlAlchemy instantiation

```python

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQL_DATABASE_URL = "sqlite:///./todos.db"

# specify the url of the sqlite database interaction and ./todos.db specify that the todos.db will be creating the current directory..

engine = create_engine(SQL_DATABASE_URL, connect_args={"check same threads": False})

# create a engine for the sqlalchemy which is the starting point of the application and (check same thread = false) specify the multiple thread option

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# this is the factory to create database session


Base = declarative_base()

# Base will be used to create the database table using the python class..
```

# Main.py file

```python

import models
from database import engine

from fastapi import FastAPI

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
# use to create the database table from the python classes..
```
