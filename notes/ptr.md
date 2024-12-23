# routing execution (path parameter issue)

```python
# fastapi execute from top to bottom
# path parameter {something} this will consume anything that comes after /todos/ and assign the value to something =
@router.get("/test") # Specific routes first
async def test(request: Request):
return templates.TemplateResponse("home.html", {"request": request})

@router.get("/{todo_id}") # Path parameters later
async def read_todo(...): # ...

#Rule of Thumb

# Put specific paths before path parameters
# More specific routes should come first
# Path parameters should come last

```

# Always try to use the absolute path in the import

- absolute import means start from the project root but does not use the root directory name (like from router.auth is absolute path example from database is also)

```python
"""
your_project/
├── **init**.py
├── main.py
├── database.py
├── models.py
└── routers/
  ├── **init**.py
  └── auth.py
  └── todos.py
"""
```

# In main.py

from routers.auth import router as auth_router

# In routers/auth.py

from database import SessionLocal
from models import Users

# In routers/todos.py

from .auth import something (relative import)

---

# Always import only the specific method instead of the entire module

### example:

- from todoapp import models (❌)
- from todos.models import users (✅)

---
