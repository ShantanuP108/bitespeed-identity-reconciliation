# app/main.py

from fastapi import FastAPI
from routes import router
from models import Base
from database import engine

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

app.include_router(router)