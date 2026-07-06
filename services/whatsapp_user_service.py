from sqlalchemy.orm import Session

from models import UserDB, WhatsAppUserDB


def get_or_create_user(
    db: Session,
    wa_id: str,
    push_name: str
) -> UserDB:

    whatsapp_user = (
        db.query(WhatsAppUserDB)
        .filter(WhatsAppUserDB.wa_id == wa_id)
        .first()
    )

    if whatsapp_user:
        return whatsapp_user.user

    new_user = UserDB(
        nama="",
        email="",
        status="BOT_MODE",
        registration_step="ASK_REGISTRATION"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    whatsapp = WhatsAppUserDB(
        wa_id=wa_id,
        user_id=new_user.id,
        push_name=push_name or ""
    )

    db.add(whatsapp)
    db.commit()

    return new_user