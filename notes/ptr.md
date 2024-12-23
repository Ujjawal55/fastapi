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
