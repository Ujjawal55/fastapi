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

  [code](code.md#L179)

# Creating a form

[code](code.md#L200)

# SqlAlchemy

- sqlAlchemy is sql toolkit and ORM for the system that provide powerful interaction with the database.

  - **_Steps:_**
    - First, you create an engine that connects to your database
    - Then you create a base class to define your database models
    - Finally, you use sessionmaker to create sessions for database operations
