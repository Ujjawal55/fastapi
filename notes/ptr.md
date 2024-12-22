# Always try to use the absolute path in the import

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
"""
```

# In main.py

from routers.auth import router as auth_router

# In routers/auth.py

from database import SessionLocal
from models import Users

---

# Always import only the specific method instead of the entire module

### example:

- from todoapp import models (❌)
- from todos.models import users (✅)

---
