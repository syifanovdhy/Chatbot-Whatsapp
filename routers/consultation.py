from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import session

from constants.states import CONSULTATION_WAITING
from dependencies import get_db
from models import ConsultationDB, MessageDB
from schemas.consultation import ConsultationCreate

router = APIRouter()

@router.post("/consultations-db")
def create_consultation_db(
    consultation: ConsultationCreate,
    db: session = Depends(get_db)
):
    new_consultation = ConsultationDB(
        user_id=consultation.user_id,
        keperluan=consultation.keperluan,
        status=CONSULTATION_WAITING
    )
    db.add(new_consultation)
    db.commit()
    db.refresh(new_consultation)
    return new_consultation

@router.get("/consultations-db")
def get_consultations_db(
    db: session = Depends(get_db)
):
    consultations = db.query(ConsultationDB).all()
    return consultations

@router.get("/consultations-db/{consultation_id}/messages")
def get_consultation_messages_db(
    consultation_id: int,
    db: session = Depends(get_db)
):
    messages = db.query(MessageDB).filter(
        MessageDB.consultation_id == consultation_id).all()
    return messages

@router.get("/test-relation/{consultation_id}")
def test_relation(
    consultation_id: int, db: 
    session = Depends(get_db)):
    
    consultation = db.query(
        ConsultationDB
        ).filter(
            ConsultationDB.id == consultation_id
            ).first()
    if not consultation:
        raise HTTPException(status_code=404, detail="Consultation not found")
    return {
        "consultation.id": consultation.id,
        "jumlah_pesan": len(consultation.messages)
    }