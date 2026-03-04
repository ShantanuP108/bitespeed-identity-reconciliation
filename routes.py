# app/routes.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from services import identify_contact
from schemas import IdentifyRequest

router = APIRouter()

@router.post("/identify")
def identify(payload: IdentifyRequest, db: Session = Depends(get_db)):
    return identify_contact(
        db,
        email=payload.email,
        phoneNumber=payload.phoneNumber
    )