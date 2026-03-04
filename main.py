# app/main.py

from fastapi import FastAPI
from app.routes import router
from app.models import Base
from app.database import engine

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

app.include_router(router)