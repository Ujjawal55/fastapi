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
