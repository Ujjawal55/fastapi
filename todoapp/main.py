import models
from database import engine
from routers.auth import router as auth_router
from routers.todos import router as todos_router

from fastapi import FastAPI

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(todos_router)
