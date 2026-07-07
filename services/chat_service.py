from sqlalchemy.orm import Session
from services.whatsapp_user_service import get_or_create_user
from services.registration_service import handle_registration

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

    print("=================================")
    print("User ID   :", user.id)
    print("WA Name   :", user.whatsapp_accounts[0].push_name)
    print("Nama PST  :", user.nama)
    print("Step      :", user.registration_step)
    print("Message   :", message)
    print("=================================")

    reply = handle_registration(
        db=db,
        user=user,
        message=message
    )

    if reply:
        return reply

    return "Belum diimplementasikan."