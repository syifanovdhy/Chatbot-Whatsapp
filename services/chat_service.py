from sqlalchemy.orm import Session
from routers import message
from services.whatsapp_user_service import get_or_create_user

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

    return "Belum diimplementasikan."