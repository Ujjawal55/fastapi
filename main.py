from starlette.staticfiles import StaticFiles

import models
from company.companyapis import router as companyapis_router
from company.dependencies import get_token_header
from database import engine
from fastapi import Depends, FastAPI
from routers.address import router as address_router
from routers.auth import router as auth_router
from routers.todos import router as todos_router

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth_router)
app.include_router(todos_router)
app.include_router(address_router)
app.include_router(
    companyapis_router,
    prefix="/company",
    tags=["companyapis"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "Internal Use only"}},
)
