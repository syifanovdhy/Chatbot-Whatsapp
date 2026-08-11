from sqlalchemy import func
from sqlalchemy.orm import Session
from models import ConsultationDB, MessageDB, ActivityLogDB, MenuLogDB
from constants.states import CONSULTATION_WAITING,CONSULTATION_ACTIVE


def get_service_statistics(
    db: Session
):

    result = (
        db.query(
            MenuLogDB.menu_type,
            func.count(MenuLogDB.id).label("jumlah")
        )
        .group_by(
            MenuLogDB.menu_type
        )
        .all()
    )

    return [
        {
            "menu": menu,
            "jumlah": jumlah
        }
        for menu, jumlah in result
    ]


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

def get_consultation_timeline(
    consultation: ConsultationDB
):

    timeline = []

    for activity in consultation.activity_logs:

        timeline.append({

            "type": "activity",

            "activity": activity.activity,

            "description": activity.description,

            "created_at": activity.created_at

        })

    for message in consultation.messages:

        timeline.append({

            "type": "message",

            "sender": message.sender,

            "content": message.content,

            "created_at": message.created_at

        })

    timeline.sort(

        key=lambda item: item["created_at"]

    )

    return timeline