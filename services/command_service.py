from sqlalchemy.orm import Session

from constants.states import MAIN_MENU, WAITING_CONSULTATION, WAITING_AGENT, BOT_MODE
from models import UserDB
from services.consultation_service import finish_consultation, get_active_consultation
from services.menu_service import get_main_menu


def handle_global_command(
    db: Session,
    user: UserDB,
    message: str,
):
    message = message.strip().lower()

    if message in ["0", "menu"]:
        user.registration_step = MAIN_MENU
        user.status = BOT_MODE
        db.commit()
        return get_main_menu()

    if message == "selesai":
        consultation = get_active_consultation(db=db, user_id=user.id)
        if consultation is None:
            return ("Terima kasih telah menggunakan layanan STATARA. 😊 \n\n"
                    "Percakapan telah selesai.\n\n"
                    "Semoga layanan kami dapat membantu kebutuhan data dan informasi Anda.\n\n"
                    "Ketik *Menu* atau *0* jika ingin menggunakan layanan STATARA kembali."
            )

        finish_consultation(db=db, consultation=consultation)
        return (
            "Konsultasi telah selesai.\n\n"
            "Terima kasih telah menggunakan layanan STATARA.\n\n"
            "Ketik *Menu* atau *0* untuk kembali ke menu utama."
        )

    if message == "batal":
        if user.registration_step == WAITING_CONSULTATION:
            user.registration_step = MAIN_MENU
            db.commit()
            return ("Permintaan konsultasi dibatalkan.\n\n"
                    "Semoga layanan kami dapat membantu kebutuhan data dan informasi Anda.\n\n"
                    "Ketik *Menu* atau *0* jika ingin menggunakan layanan STATARA kembali."
                )

        if user.registration_step == WAITING_AGENT:
            consultation = get_active_consultation(db=db, user_id=user.id)
            if consultation is not None and not consultation.agent_replied:
                finish_consultation(db=db, consultation=consultation)
                return (
                    "Permintaan konsultasi dibatalkan.\n\n"
                    + get_main_menu()
                )

            return (
                "Petugas sudah membalas konsultasi Anda.\n\n"
                "Ketik *selesai* jika ingin mengakhiri konsultasi."
            )

    return None
