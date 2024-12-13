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
