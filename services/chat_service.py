from sqlalchemy.orm import Session
from constants.states import AGENT_MODE, PUBLICATION_MENU
from services.agent_service import handle_agent_mode
from services.command_service import handle_global_command
from services.whatsapp_user_service import get_or_create_user
from services.registration_service import handle_registration
from services.menu_service import handle_main_menu
from services.consultation_service import handle_consultation
from constants.states import DATA_MENU

def process_chat(
    db: Session,
    message: str,
    wa_id: str,
    push_name: str
):

    user = get_or_create_user(
        db=db,
        wa_id=wa_id,
        push_name=push_name
    )

    # Perintah global
    reply = handle_global_command(
        db=db,
        user=user,
        message=message
    )

    if reply:
        return reply

    # Mode petugas
    if user.status == AGENT_MODE:

        return handle_agent_mode(
            db=db,
            user=user,
            message=message
        )

    reply = handle_registration(
        db=db,
        user=user,
        message=message
    )

    if reply:
        return reply

    reply = handle_main_menu(
        db=db,
        user=user,
        message=message
    )

    if reply:
        return reply

    if user.registration_step == PUBLICATION_MENU:
        from services.publication_service import handle_publication

        reply = handle_publication(
            db=db,
            user=user,
            message=message
        )

        if reply:
            return reply

    if user.registration_step == DATA_MENU:
        from services.data_service import handle_data

        reply = handle_data(
            db=db,
            user=user,
            message=message
        )

        if reply:
            return reply

    reply = handle_consultation(
        db=db,
        user=user,
        message=message
    )

    if reply:
        return reply

    return (
        "Maaf, saya belum memahami pesan tersebut.\n\n"
        "Ketik *0* untuk kembali ke menu utama."
    )