from sqlalchemy.orm import Session

from models import UserDB

from constants.states import (
    MAIN_MENU,
    WAITING_CONSULTATION,
    WAITING_AGENT,
    BOT_MODE
)

from services.menu_service import get_main_menu


def handle_global_command(
    db: Session,
    user: UserDB,
    message: str
):
    message = message.strip().lower()

    # =========================
    # Kembali ke menu utama
    # =========================
    if message in ["0", "menu"]:

        user.registration_step = MAIN_MENU
        user.status = BOT_MODE

        db.commit()

        return get_main_menu()

    # =========================
    # Batalkan proses
    # =========================
    if message == "batal":

        if user.registration_step == WAITING_CONSULTATION:

            user.registration_step = MAIN_MENU

            db.commit()

            return (
                "✅ Permintaan konsultasi dibatalkan.\n\n"
                + get_main_menu()
            )

        if user.registration_step == WAITING_AGENT:

            return (
                "❌ Konsultasi sudah dikirim ke petugas.\n\n"
                "Silakan tunggu balasan petugas atau ketik *selesai* jika ingin mengakhiri konsultasi."
            )

    return None