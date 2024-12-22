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

---

# session creation and handing...

```python

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

import models
from database import SessionLocal, engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def read_all(db: Session = Depends(get_db)):

# FastAPI automatically:
    # 1. Calls get_db(): when the fast api see the get_db() method in the parameter call the method
    # 2. Gets the yielded session:

       # It allows the database session to be used in the route function.
       # After the route function completes, execution returns to get_db() to close the session

    # after the yield is executed the read_all() method have the access to the db and the get_db() method holds for the operation of the read_all()(router function) to complete
    # after the completion and control back to the get_db() method and it finally closes the session...

    return db.query(models.Todo).all()

```

---

# creating the post request...

```python

# create the pydantic class that is used for the validation of the incoming data in the post request...
class TodoCreate(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(
        ge=1, le=5, description="priority should be in between 1 and 5"
    )
    complete: bool


# post request to create the todo
@app.post("/")
async def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = models.Todo(
        title=todo.title,
        description=todo.description,
        priority=todo.priority,
        complete=todo.complete,
    )

    db.add(db_todo) # create the instance without commit it the database

    db.commit() # commit the changes to the database...

    return {"status_code": 201, "message": "record has been successfully created"}
```

---

# PUT Request

```python
@app.put("/{todo_id}")
async def update_todo(todo_id: int, todo: TodoCreate, db: Session = Depends(get_db)):
    # get the particular instance of the data
    todo_model = db.query(models.Todo).filter(models.Todo.id == todo_id).first()

    if todo_model is None:
        raise http_exception_404()

    todo_model.title = todo.title  # type: ignore
    todo_model.description = todo.description  # type: ignore
    todo_model.priority = todo.priority  # type: ignore
    todo_model.complete = todo.complete  # type: ignore

    db.add(todo_model)
    db.commit()

    return {"status": 200, "message": "successful"}
```

---

# Delete request

```python

# delete request
@app.delete("/{todo_id}")
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo_model = db.query(models.Todo).filter(models.Todo.id == todo_id).first()

    if todo_model is None:
        raise http_exception_404()

    db.delete(todo_model) # first create a object for deletetion then commit the changes to the database..
    db.commit()
    return http_status_code_200()


def http_status_code_200():
    return {"status": 200, "message": "successfull"}
```

---

# Relationship

### one-to-one relationship

```python
class User(Base):
  id = Column(Integer, primary_key=True)
  profile = relationship("Profile", uselist=False, back_populates="user")

class Profile(Base):
  id = Column(Integer, primary_key=True)
  user_id = Column(Integer, ForeignKey("user.id"), unique=True)
  user = relationship("User", back_populates="profile")

```

### one-to-many relationship

```python

class User(Base):
    id = Column(Integer, primary_key=True)
    posts = relationship("Post", back_populates="user")

class Post(Base):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="posts")
```

### many-to-many relationship

```python

user_groups = Table(
    "user_groups", Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("group_id", Integer, ForeignKey("groups.id"))
)

class User(Base):
    id = Column(Integer, primary_key=True)
    groups = relationship("Group", secondary=user_groups, back_populates="users")

class Group(Base):
    id = Column(Integer, primary_key=True)
    users = relationship("User", secondary=user_groups, back_populates="groups")
```

# Example of Relationship in FastAPI

```python
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hassed_password = Column(String)
    is_active = Column(Boolean, default=True)

    todos = relationship("Todo", back_populates="owner")

#NOTE: the back_populates name should match with the attribute name of the other class

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("Users", back_populates="todos")
```

---

# Authentication

```python

from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

import models

# ------------------------------------------------***Password Hashing****-----------------------------

from passlib.context import CryptContext
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hassed_password(password):
  return bcrypt_context.hash(password)

# ----------------------------------------------*****----------------------------------------

# Pydantic class for the data validation

class UserCreate(BaseModel):

    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    hassed_password: str


app = FastAPI()


@app.post("/create/user")
async def create_new_user(user: UserCreate):
    user_model = models.Users(
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        hassed_password=get_hassed_password(user.hassed_password),
        is_active=True,
    )

    return user_model

```

---

# Verification of user

```python

def verify_hashed_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)


def is_user_exist(username: str, password: str, db) -> bool:
    user = db.query(models.Users).filter(models.Users.username == username).first()

    if not user:
        return False
    if not verify_hashed_password(password, user.hashed_password):
        return False
    return user

@app.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):

  #NOTE: OAuth2PasswordRequestForm is a library to import from fastapi.security

    user = is_user_exist(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    return "user validated"


```

---

# Access token creation

```python

from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt

SECERT_KEY = "put_hash_value_in_here"
ALGORITHM = "HS256"

def create_access_token(
    username: str, user_id: int, expire_delta: Optional[timedelta] = None
):

    # encode is the message that you want jwt to hold
    encode = {"sub": username, "id": user_id}

    # setting up the basic expire_delta value so that it can be added to the jwt
    if expire_delta:
        expire = datetime.utcnow() + expire_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    encode.update({"exp": expire})

    return jwt.encode(encode, SECERT_KEY, algorithm=ALGORITHM)


@app.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = is_user_exist(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    token_expires = timedelta(minutes=15)
    token = create_access_token(user.username, user.id, expire_delta=token_expires)

    return {"token": token}
```

---

# GET CURRENT USER

```python
from jose import JWTError

async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECERT_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub", None)
        user_id = payload.get("id", None)
        if username is None or user_id is None:
            raise HTTPException(status_code=404, detail="User not found")
        return {
            "username": username,
            "user_id": user_id,
        }

    except JWTError:
        raise HTTPException(status_code=404, detail="User not found")
```

---

# Authentication method for getting the todo of the user.

```python

@app.get("/todos/user")
async def read_all_by_user(
    user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):

    if user is None:
        raise HTTPException(status_code=404, detail="user not found")

    return (
        db.query(models.Todo).filter(models.Todo.owner_id == user.get("user_id")).all()
    )
```

---

# Authentication before returing the todo.

```python

@app.get("/todo/{todo_id}")
async def read_todo(
    todo_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)
):
    if user is None:
        raise http_exception_404()

    todo = (
        db.query(models.Todo)
        .filter(models.Todo.id == todo_id)
        .filter(models.Todo.owner_id == user.get("user_id"))
        .first()
    )
    if todo is not None:
        return todo
    raise http_exception_404()

```

---

## command to create the postgresql table...

```sql
drop table if exists users;

create table users (
	id serial,
	email varchar(200) default null,
	username varchar(45) default null,
	first_name varchar(45) default null,
	last_name varchar(45) default null,
	hashed_password varchar(200) default null,
	is_active boolean default null,
	primary key(id)
);

drop table if exists todos;

create table todos (
	id serial,
	title varchar(45) default null,
	description varchar(200) default null,
	priority integer default null,
	complete boolean default null,
	owner_id integer default null,
	primary key(id),
	foreign key (owner_id) references users(id)
);
```

---

# Connect FASSTAPI to postgres

```python
#NOTE: database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQL_DATABASE_URL = "postgresql://postgres:pan123@localhost/TodoApplicationDatabse"

engine = create_engine(SQL_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()
```
