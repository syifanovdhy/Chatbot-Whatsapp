from pydantic import BaseModel
from fastapi import APIRouter, Depends
from dependencies import get_db
from models import MenuLogDB, UserDB, ConsultationDB
from sqlalchemy.orm import Session
from services.menu_service import process_menu_choice, get_menu_name
from services.whatsapp_user_service import get_or_create_user
from services.registration_service import process_registration

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    wa_id: str
    push_name: str = ""

@router.post("/chat")
def chat(
    request: ChatRequest, 
    db: Session = Depends(get_db)
):
    user = get_or_create_user(
    db=db,
    wa_id=request.wa_id,
    push_name=request.push_name
)
    if user.registration_step in [
    "ASK_NAME",
    "ASK_INSTITUTION",
    "ASK_EMAIL"
    ]:

        if (
            user.registration_step == "ASK_NAME"
            and request.message.lower()
            in ["halo", "hai", "hi", "assalamualaikum"]
        ):

            return {
                "reply":
                (
                    "👋 Selamat datang di Pelayanan Statistik Terpadu BPS Kabupaten Banggai Kepulauan.\n\n"
                    "Perkenalkan, saya PST Bot yang akan membantu Anda.\n\n"
                    "Sebelum menggunakan layanan, boleh ketik *nama lengkap* Anda?"
                )
            }

        reply = process_registration(
            db=db,
            user=user,
            message=request.message
        )

        return {
            "reply": reply
        }

    menu_name = get_menu_name(request.message)
    if menu_name:
        log = MenuLogDB(
            user_id=user.id,
            menu=menu_name
        )
        db.add(log)
        db.commit()
    
    if request.message == "2":

        consultation = ConsultationDB(
            user_id=user.id,
            keperluan="Menunggu deskripsi",
            status="waiting_agent"
        )

        db.add(consultation)
        db.commit()

    reply = process_menu_choice(request.message)

    return {
        "reply": reply
    }