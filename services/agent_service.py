from sqlalchemy.orm import Session

from models import (
    UserDB
)

from services.consultation_service import (
    get_active_consultation,
    save_user_message
)

def handle_agent_mode(
    db: Session,
    user: UserDB,
    message: str
):
    consultation = get_active_consultation(
        db=db,
        user_id=user.id
    )

    if consultation is None:

        return (
            "Mohon tunggu petugas."
        )

    save_user_message(
        db=db,
        consultation=consultation,
        message=message
    )

    return None