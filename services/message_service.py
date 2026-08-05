from sqlalchemy.orm import Session

from constants.activity_types import AGENT_REPLY
from constants.states import AGENT_MODE, CONSULTATION_ACTIVE
from models import (
    ConsultationDB,
    MessageDB,
    WhatsAppUserDB
)

from constants.message_types import (
    SENDER_USER,
    SENDER_AGENT
)

from routers import message
from services.activity_services import add_activity
from services.whatsapp_gateway import (
    send_whatsapp_message
)

def add_agent_message(
    db: Session,
    consultation: ConsultationDB,
    message: str
):
    new_message = MessageDB(
        consultation_id=consultation.id,
        sender=SENDER_AGENT,
        content=message
    )

    db.add(new_message)
    db.commit()

    add_activity(
        db=db,
        consultation=consultation,
        activity=AGENT_REPLY,
        description="Petugas membalas"
    )

def send_agent_reply(
    db: Session,
    consultation: ConsultationDB,
    message: str
):
    wa_account = consultation.user.whatsapp_accounts[0]

    send_whatsapp_message(
        wa_account.wa_id,
        message
    )

    add_agent_message(
        db,
        consultation,
        message
    )

    consultation.agent_replied = True
    consultation.status = CONSULTATION_ACTIVE
    consultation.user.status = AGENT_MODE

    db.commit()

    return True