from sqlalchemy.orm import Session
from models import ConsultationDB
from constants.states import (
    CONSULTATION_WAITING,
    CONSULTATION_ACTIVE
)


def get_waiting_consultations(
    db: Session
):

    return (
        db.query(ConsultationDB)
        .filter(
            ConsultationDB.status.in_([
                CONSULTATION_WAITING,
                CONSULTATION_ACTIVE
            ])
        )
        .order_by(
            ConsultationDB.started_at.desc()
        )
        .all()
    )