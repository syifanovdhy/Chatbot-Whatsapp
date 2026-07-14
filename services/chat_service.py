from sqlalchemy.orm import Session
from services.whatsapp_user_service import get_or_create_user
from services.registration_service import handle_registration
from services.menu_service import handle_main_menu
from services.consultation_service import handle_consultation

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

    # print("=================================")
    # print("User ID   :", user.id)
    # print("WA Name   :", user.whatsapp_accounts[0].push_name)
    # print("Nama PST  :", user.nama)
    # print("Step      :", user.registration_step)
    # print("Message   :", message)
    # print("=================================")

    reply = handle_registration(
        db=db,
        user=user,
        message=message
    )

    if reply:
        return reply
    
    reply = handle_main_menu(
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