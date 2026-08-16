from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_db
from sqlalchemy.orm import Session
from models import UserDB, WhatsAppUserDB
from schemas import user
from services.consultation_service import get_active_consultation
from services.message_service import record_agent_reply

router = APIRouter()

class AgentModeRequest(BaseModel):
    user_id: int


class DirectAgentReplyRequest(BaseModel):
    wa_id: str
    message: str


@router.post("/agent/direct-reply")
def record_direct_reply(
    request: DirectAgentReplyRequest,
    db: Session = Depends(get_db),
):
    whatsapp_user = (
        db.query(WhatsAppUserDB)
        .filter(WhatsAppUserDB.wa_id == request.wa_id)
        .first()
    )

    if whatsapp_user is None:
        return {"recorded": False, "reason": "user_not_found"}

    consultation = get_active_consultation(
        db=db,
        user_id=whatsapp_user.user_id,
    )
    if consultation is None:
        return {"recorded": False, "reason": "no_active_consultation"}

    record_agent_reply(
        db=db,
        consultation=consultation,
        message=request.message,
    )
    return {"recorded": True, "consultation_id": consultation.id}

@router.post("/agent/take-over")
def take_over(
    request: AgentModeRequest,
    db: Session = Depends(get_db)
):
    user = db.get(
    UserDB,
    request.user_id
    )
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User tidak ditemukan"
        )
    user.status = "AGENT_MODE"

    db.commit()

    return {
        "message": "User diambil alih petugas"
    }

@router.post("/agent/release")
def release(
    request: AgentModeRequest,
    db: Session = Depends(get_db)
):
    user = db.get(
    UserDB,
    request.user_id
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User tidak ditemukan"
        )

    user.status = "BOT_MODE"

    db.commit()

    return {
        "message": "Kembali ke bot"
    }
        
