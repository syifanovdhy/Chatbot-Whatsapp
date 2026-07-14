from sqlalchemy.orm import Session

from models import ConsultationDB

def get_waiting_consultations(
    db: Session
):

    return (
        db.query(ConsultationDB)
        .order_by(
            ConsultationDB.started_at.desc()
        )
        .all()
    )

