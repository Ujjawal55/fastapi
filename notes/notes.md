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
