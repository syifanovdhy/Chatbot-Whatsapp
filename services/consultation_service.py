from sqlalchemy.orm import Session
from constants.message_types import SENDER_USER
from models import ConsultationDB, MessageDB
from models import UserDB

from constants.states import (
    CONSULTATION_STATUS_WAITING_AGENT,
    MAIN_MENU,
    WAITING_CONSULTATION,
    WAITING_AGENT
)
from services.menu_service import get_main_menu

def handle_consultation(
    db: Session,
    user: UserDB,
    message: str
):

    if user.registration_step == MAIN_MENU:

        if message != "2":
            return None

        user.registration_step = WAITING_CONSULTATION

        db.commit()

        return (
            "📞 *Konsultasi Statistik*\n\n"
            "Silakan tuliskan pertanyaan atau kebutuhan konsultasi Anda.\n\n"
            "Contoh:\n"
            "- Memerlukan data IPM tahun 2025\n"
            "- Cara menggunakan data BPS\n"
            "- Permintaan data statistik tertentu"
        )
    
    if user.registration_step == WAITING_CONSULTATION:

        consultation = ConsultationDB(
            user_id=user.id,
            keperluan=message,
            status="waiting_agent"
        )

        db.add(consultation)
        db.commit()
        db.refresh(consultation)

        first_message = MessageDB(
            consultation_id=consultation.id,
            sender="user",
            content=message
        )

        db.add(first_message)

        user.registration_step = WAITING_AGENT

        db.commit()

        return (
            "✅ Permintaan konsultasi telah diterima.\n\n"
            "Petugas PST akan segera membalas pesan Anda.\n\n"
            "Mohon tunggu beberapa saat."
        )
    
    if user.registration_step == WAITING_AGENT:

        consultation = get_active_consultation(
            db=db,
            user_id=user.id
        )

        if consultation is None:

            user.registration_step = MAIN_MENU

            db.commit()

            return get_main_menu()

        save_user_message(
            db=db,
            consultation=consultation,
            message=message
        )

    return (
        "📩 Pesan Anda telah ditambahkan ke konsultasi yang sedang berlangsung.\n\n"
        "Petugas PST akan segera membalas."
    )

    return None

def save_user_message(
    db: Session,
    consultation: ConsultationDB,
    message: str
):

    new_message = MessageDB(
        consultation_id=consultation.id,
        sender=SENDER_USER,
        content=message
    )

    db.add(new_message)
    db.commit()

def get_active_consultation(
    db: Session,
    user_id: int
):

    return (
        db.query(ConsultationDB)
        .filter(
            ConsultationDB.user_id == user_id,
            ConsultationDB.status == CONSULTATION_STATUS_WAITING_AGENT
        )
        .order_by(ConsultationDB.started_at.desc())
        .first()
    )
    