from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import get_db
from models import ConsultationDB
from services.dashboard_service import get_waiting_consultations
from services.whatsapp_gateway import send_whatsapp_message
from models import WhatsAppUserDB
from pydantic import BaseModel

class ReplyRequest(BaseModel):
    message: str

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

@router.post("/test-send/{user_id}")
def test_send(
    user_id: int,
    db: Session = Depends(get_db)
):

    wa_user = (
        db.query(WhatsAppUserDB)
        .filter(
            WhatsAppUserDB.user_id == user_id
        )
        .first()
    )

    if wa_user is None:
        return {
            "success": False,
            "message": "WA tidak ditemukan"
        }

    result = send_whatsapp_message(
        wa_user.wa_id,
        "Halo 👋 ini pesan percobaan dari Dashboard PST."
    )

    return result

@router.post(
    "/consultations/{consultation_id}/reply"
)
def reply_consultation(
    consultation_id: int,
    request: ReplyRequest,
    db: Session = Depends(get_db)
):

    consultation = db.get(
        ConsultationDB,
        consultation_id
    )

    if consultation is None:

        return {
            "success": False
        }

    from services.message_service import (
        send_agent_reply
    )

    send_agent_reply(
        db,
        consultation,
        request.message
    )

    return {
        "success": True
    }

@router.post(
    "/consultations/{consultation_id}/finish"
)
def finish_consultation_api(
    consultation_id: int,
    db: Session = Depends(get_db)
):

    consultation = db.get(
        ConsultationDB,
        consultation_id
    )

    if consultation is None:

        return {
            "success": False
        }

    from services.consultation_service import (
        finish_consultation
    )

    finish_consultation(
        db=db,
        consultation=consultation
    )

    return {
        "success": True
    }