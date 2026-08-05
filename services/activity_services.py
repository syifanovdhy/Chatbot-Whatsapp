from sqlalchemy.orm import Session

from models import (
    ConsultationDB,
    ActivityLogDB
)


def add_activity(
    db: Session,
    consultation: ConsultationDB,
    activity: str,
    description: str
):

    log = ActivityLogDB(

        consultation_id=consultation.id,

        activity=activity,

        description=description

    )

    db.add(log)

    db.commit()