# 11 December 2024

- what is fastapi
- how to activate the virtual env
- install the dependency for the fastapi

# Enumeration concept

- help to predefined the value of the variable and we can use to restrict the domain of a variable
- [code](code.md)

# Query Parameter vs Path parameter

- **Path Parameter:** This is part of the endpoint itself. It is often used to identify a specific resource or action and is an essential part of the URL.
- **Query Parameter:** This is additional data that is appended to the endpoint, typically to modify or filter the results of the endpoint.

---

# 12 December 2024

- setup the new project2 with the pydantic \*\*(Python library for the data validation and settings)

# pydantic data validation

- when define a class object using pydantic and use the class object as parameter, the fastapi automatically assume that we send the data in the body
  [code](code.md#L82)

# Field class from pydantic

- it is used to **specify constraint** on the pydantic model attribute and pydantic validate against those constraint automatically.

# class Config of BaseModel

- **class Config:** is a part of BaseModel which is used to change the default of BaseModel for data serailization, enforcing strict data types and how model behave during initialization(what example show on by default for post request).
- config class should be nested inside the pydantic model
- **NOTE:** In verson(V2+) the way to define the example configuration for pydantic model has been changed..
  [code](code.md#L101)

# 12 December 2024

# HTTPException

- declare a function to be used if the task is to repeat

  [code](notes.md#L118)

# Custom Exception

### steps

- first step is define a class **_(above the app declaration)_** that inherit the built-in Exception from fastapi
  - define the attribute in the **\_\_init\_\_** for extra information in the error message.
- second define a exception decorator just below the **app** definition
  - use of the definition to tell fastapi what to do when the exception occur.

[code](code.md#L132)

# Response model class

- **Defination**: A Response Model in FastAPI is a crucial feature that defines and controls the structure of data returned by your API endpoints.

  - if more data present in the return then fastapi will automatically filter out the extra data compare to the **response class attribute**

  ## NOTE: you have to return the data object which matches the response class when you use it in the decorator..

  [code](code.md#L179)

# Creating a form

[code](code.md#L200)

# SqlAlchemy

- sqlAlchemy is sql toolkit and ORM for the system that provide powerful interaction with the database.

  - **_Steps:_**
    - First, you create an engine that connects to your database
    - Then you create a base class to define your database models
    - Finally, you use sessionmaker to create sessions for database operations

# command to create the todo.db

### models.Base.metadata.create_all(bind=engine):

- Ensures that all tables defined in your models.py file (inheriting from Base) are created in the database file (todos.db).
- run the main.py file containing the (models.Base.metadata.create_all(bind=engine) command to create the todo.db file

# 17 December 2024

# creating a session

- session is important for the route(incoming http request) with database request.
- In fastAPI we have to manage the session opening and closing manually.
  [code](code.md#L258)

---

# 18 December 2024

# Creating a POST request to the database.

- in order to create a post request to the model we need the pydantic model.
- a pydantic model is similar to the SQLAlchemy model but used for the database validation(similar to form in the django)..
  [code](code.md#L298)

# Relationship in sqlAlchemy

1. first create foreginkey in the related schema(table).
2. define the both side connection.
3. define the back_populates.
   [code](code.md#L380)

# Creating a user in the database.

1. create a new file auth.py
2. first create the pydantic class for the validation
3. write the logic of the post method
4. use the library **_passlib\[bcrypt\]_** for password hashing..

   - command to install **pip install <"passlib\[bcrypt\]\">**

[code](code.md#L466)

# Verification of user

[code](code.md#L517)

# Creating the JWT token

1. install the library "python-jose\[cryptography"\]
2. import
   - from fastapi.security import OAuth2PasswordBearer
   - from datetime import datatime, timedelta
   - from jose import jwt
3. Create Two variable
   - SECERT_KEY = "<any random value>"(try to use some has value of your particular string)
   - ALGORITHM = "HS256"
   - oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")
4. create_access_token_function() [code](code.md#L554)
5. create the token and return it.

# GET CURRENT USER

[code](code.md#L599)

---

# 20 December 2024

# USe postman to get the todo of user

1. create the database and link the data using the sqlite3 terminal.
2. write the authentication method and return the data from the database.

[code](code.md#L623)

# Modification in the get todo using the todo id

- added the feature to verify the user before returning the todo.
  [code](code.md#L642)

---

# 21 December 2024

# downloading the postgresql database and gui.

### command to install the postgresql serve

1. sudo pacman -S postgresql

2. sudo mkdir /var/lib/postgres/data
   sudo chown postgres:postgres /var/lib/postgres/data
   sudo -u postgres initdb -D /var/lib/postgres/data

3. sudo systemctl start postgresql
   sudo systemctl enable postgresql

### command to install the pgadmin4

1. install the python311 in the system (yay -S python311)
2. create a virtual env (python3.11 -m venv <name of env>)
3. install the pgadmin4 (pip install pgadmin4)
4. run the pgadmin4 local server

### setup process

1. first create a host.

- sudo -u postgres psql
- CREATE USER ujjawal17032002 WITH PASSWORD 'your_password'; ALTER USER ujjawal17032002 WITH SUPERUSER;

2. modify the pg_hba.conf file..

- sudo vim /var/lib/postgres/data/pg_hba.conf
- host all ujjawal17032002 127.0.0.1/32 md5(add this line)

3. change the postgresql.conf file

- listen_addresses = "\*"
- port = 5432
- password_encryption = md5

4. sudo systemctl restart postgresql

---

# 22 December 2024

# Command to create the postgresql database

[code](code.md#L667)

# Steps to connect the postgresql to FASTAPI

1.  install the psycopg2 (pip install psycopg2-binary)(if latest version gives error install 2.9 version)
2.  set sqlachemy_database_url(variable in database.py) -> "postgresql://{username}:{password}@localhost/{databasename}"
3.  set the engine vallue -> create engine(sqlachemy_database_url)
4.  run the auth module (uvicorn auth:app --reload)
5.  create the user from the api.
6.  check the user in the pgadmin4
    [code](code.md#L699)

# Routing

- routing is like in django (in the urls.py file (project_level) we says if "\user" is hit we move to this app) this is called routing..

#### for our project we creating routing of the auth file and add that router in the main.py file

```python
# urls.py

from django.urls import path
from . import views

urlpatterns = [
path('users/', views.user_list, name='user-list'),
path('users/<int:pk>/', views.user_detail, name='user-detail'),
]

# views.py

def user_list(request):
return JsonResponse({"users": ["user1", "user2"]})

def user_detail(request, pk):
return JsonResponse({"user": f"user{pk}"})

------------------------------------------------------------------------------------------------------------

from fastapi import APIRouter

router = APIRouter(prefix="/users")

@router.get("/")
def user_list():
    return {"users": ["user1", "user2"]}

@router.get("/{user_id}")
def user_detail(user_id: int):
    return {"user": f"user{user_id}"}
```

# 23 December 2024

# Router prefix

- router prefix add the common prefix to all the routes in routers
  [code](code.md#L720)

# Verification before giving response to the company api

- every time someone try to access the company api we ask check for some security measure here we are checking if we have the somekey in the header
- create the dependecies.py file in the company directories, write the logic and add that method in the router(main.py) as dependencies.

  [code](code.md#L732)

# Installing alembic

- database migration tools specifically designed for the sqlalchemy for the database migration control
- installation process
  - pip install alembic
- Initialization
  - alembic init {directory_name} (here it is alembic)

# few changes so that the alembic will be connected to the postgresql database

- alembic.ini
  - sqlalchemy.url = {url value from the database}
- alembic/env.py
  - import models
  - config = context.config (config the defualt)
  - fileConfig(config.config_file_name) (config the defualt)
  - target_metadata = models.Base.metadata

# Changing existing user table using alembic

### Adding the phone_number column in the user table

- create a revision file (command: alembic revision -m "create phone number for user col")
  - create a new file under the alembic/versions/
- write the code for the upgrade method
  - for upgrade use the command (alembic upgrade {version_name})
- write the code for the downgrade method
  - for downgrade use the command (alembic downgrade -1)

---

**\*\***\*\***\*\***\*\*\*\***\*\***\*\***\*\***FULLSTACK\***\*\*\*\*\*\*\***\*\*\***\*\*\*\*\*\*\***\*\*\*\*\***\*\*\*\*\*\*\***\*\*\***\*\*\*\*\*\*\***

# SOME POINTS TO REMEMBER IN THE FASTAPI

- in the fastapi we define the (different http method seprately for a single route)
  - depending upon the method different function is get executed.

## some installation

- pip install jinja2(template rendering engine for python)
- pip install aiofiles(support asyncronous static files support for fastapi)

# importance of the response_class

- response class is used to control the output of the router
- by default it try to serialize the return type to json if nothing is mentioned
- **HTTPResponse** : meaning we are telling that this router will return the raw html file

# Method to use the template

- define the templates directory in the root files.
- initialize the templates in the file you want to use it
  - templates = Jinja2Templates(directory="templates")
- example..

```python
# make the necessary import

templates = Jinja2Templates(directory="templates")
@router.get("/", response_class=HTMLResponse)
async def read_all_by_user(request: Request, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND) # redirection

    todos = db.query(models.Todo).filter(models.Todo.owner_id == user.get("id")).all()

    return templates.TemplateResponse( #template response
        "home.html", {"request": request, "todos": todos, "user": user} # always pass the request in the context dictionary it is mandatory
    )

```

# To add static file in the fastapi

- add the mount point in the main.py file
  - app.mount("/static", StaticFiles(directory="static"), name="static")

# Different ways to use the form and extract data from it.

---

## 1. Using `Form` Dependency

The `Form` dependency from FastAPI is designed to extract form data from requests with the `application/x-www-form-urlencoded` content type.

### Example:

```python
from fastapi import FastAPI, Form

app = FastAPI()

@app.post("/submit-form/")
async def submit_form(name: str = Form(...), email: str = Form(...)):
    return {"name": name, "email": email}
```

---

## 2. Using `Pydantic` Models

You can define a Pydantic model to represent the structure of the form fields. This is more readable and reusable for larger forms.

### Example:

```python
from fastapi import FastAPI, Depends
from pydantic import BaseModel

class FormData(BaseModel):
    name: str
    email: str

app = FastAPI()

@app.post("/submit-form/")
async def submit_form(data: FormData = Depends()):
    return data
```

---

## 3. Using `Request` Object

The `Request` object allows manual handling of form data, providing more flexibility for dynamic or custom scenarios.

### Example:

```python
from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/submit-form/")
async def submit_form(request: Request):
    form_data = await request.form()
    name = form_data.get("name")
    email = form_data.get("email")
    return {"name": name, "email": email}
```

---

## 4. Combining `Form` with File Uploads

Handle forms that include text fields and file uploads using a combination of `Form` and `File`.

### Example:

```python
from fastapi import FastAPI, Form, File, UploadFile

app = FastAPI()

@app.post("/upload/")
async def upload_file(
    name: str = Form(...),
    file: UploadFile = File(...)
):
    return {"name": name, "filename": file.filename}
```

---

## 5. Using Query Parameters for Form Data

For simple cases, some form fields can be passed as query parameters.

### Example:

```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/submit-form/")
async def submit_form(name: str, email: str):
    return {"name": name, "email": email}
```

---

## 6. Using `multipart/form-data`

Handle forms encoded in `multipart/form-data`, especially useful for file uploads and binary data.

### Example:

```python
from fastapi import FastAPI, Form, File

app = FastAPI()

@app.post("/submit-multipart/")
async def submit_multipart(
    name: str = Form(...),
    file: bytes = File(...)
):
    return {"name": name, "file_size": len(file)}
```

---

## 7. Using Third-Party Libraries

For advanced scenarios, integrate third-party libraries like `FormData` to handle complex or nested forms.

### Example:

```python
from starlette.datastructures import FormData
from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/dynamic-form/")
async def dynamic_form(request: Request):
    form_data = await request.form()
    return {key: value for key, value in form_data.items()}
```
