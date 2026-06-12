from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies import get_db
from models import UserDB, ConsultationDB, MessageDB, MenuLogDB

router = APIRouter()


@router.get("/stats")
def get_stats(
    db: Session = Depends(get_db)
):
    unique_users = db.query(UserDB).count()
    total_consultations = db.query(ConsultationDB).count()
    total_messages = db.query(MessageDB).count()

    logs = db.query(MenuLogDB).all()
    menu_stats = {
        "PERPUSTAKAAN": 0,
        "KONSULTASI": 0,
        "SILASTIK": 0,
        "ROMANTIK": 0,
        "PENGADUAN": 0
    }

    for log in logs:
        if log.menu_type in menu_stats:
            menu_stats[log.menu_type] += 1

    return {
        "unique_users": unique_users,
        "total_consultations": total_consultations,
        "total_messages": total_messages,
        "menu_stats": menu_stats
    }