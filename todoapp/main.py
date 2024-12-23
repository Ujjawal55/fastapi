import models
from company.companyapis import router as companyapis_router
from database import engine
from routers.auth import router as auth_router
from routers.todos import router as todos_router

from fastapi import FastAPI

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(todos_router)
app.include_router(
    companyapis_router,
    prefix="/company",
    tags=["companyapis"],
    responses={418: {"description": "Internal Use only"}},
)
