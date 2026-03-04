# app/routes.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import identify_contact
from app.schemas import IdentifyRequest

router = APIRouter()

@router.post("/identify")
def identify(payload: IdentifyRequest, db: Session = Depends(get_db)):
    return identify_contact(
        db,
        email=payload.email,
        phoneNumber=payload.phoneNumber
    )