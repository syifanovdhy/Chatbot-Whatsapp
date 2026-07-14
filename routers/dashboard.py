from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import get_db
from models import ConsultationDB
from services.dashboard_service import (
    get_waiting_consultations
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/consultations")
def dashboard_consultations(
    db: Session = Depends(get_db)
):

    consultations = get_waiting_consultations(db)

    result = []

    for consultation in consultations:

        result.append({

            "id": consultation.id,

            "nama": consultation.user.nama,

            "instansi": consultation.user.instansi,

            "status": consultation.status,

            "started_at": consultation.started_at

        })

    return result

@router.get(
    "/consultations/{consultation_id}"
)
def consultation_detail(
    consultation_id: int,
    db: Session = Depends(get_db)
):

    consultation = (
        db.query(ConsultationDB)
        .filter(
            ConsultationDB.id == consultation_id
        )
        .first()
    )

    if consultation is None:

        return {
            "detail":"Consultation not found"
        }

    return {

        "id": consultation.id,

        "nama": consultation.user.nama,

        "instansi": consultation.user.instansi,

        "status": consultation.status,

        "messages":[

            {

                "sender": message.sender,

                "content": message.content

            }

            for message
            in consultation.messages

        ]

    }