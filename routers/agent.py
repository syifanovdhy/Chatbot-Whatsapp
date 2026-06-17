from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_db
from sqlalchemy.orm import Session
from models import UserDB
from schemas import user

router = APIRouter()

class AgentModeRequest(BaseModel):
    user_id: int

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
        
