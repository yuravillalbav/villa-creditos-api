from fastapi import FastAPI

from models import models
from database.connection import engine
from routers import routers as loan_routers

def init_db():
    models.Base.metadata.create_all(bind=engine)

init_db()

app = FastAPI(

    title="Villa Créditos API",
    description="API para la gestión de préstamos personales con FastAPI",
    version="1.0.0"

)

app.include_router(loan_routers.router)