from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies import get_db
from models import ConsultationDB
from routers import consultation

router = APIRouter()

@router.get("/check-timeouts")
def check_timeouts(
    db: Session = Depends(get_db)
):
    consultations = db.query(
    ConsultationDB
).filter(
    ConsultationDB.status == "waiting_agent"
).all()
    timed_out = []
    for consultation in consultations:
        if consultation.timeout_sent:
            continue
        deadline = (
            consultation.started_at + timedelta(minutes=5)
            )
        if datetime.utcnow() > deadline:
            consultation.status = "timeout"
            consultation.timeout_sent = True
            timed_out.append({
                "consultation_id": consultation.id,
                "user_id": consultation.user_id
            })
    db.commit()
    return{
        "timed_out_consultations": timed_out
    }
