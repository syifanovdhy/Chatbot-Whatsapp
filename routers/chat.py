from urllib import request

from pydantic import BaseModel
from fastapi import APIRouter, Depends
from dependencies import get_db
# from models import MenuLogDB, UserDB, ConsultationDB
from sqlalchemy.orm import Session
# from services.menu_service import get_main_menu, process_menu_choice, get_menu_name
# from services.whatsapp_user_service import get_or_create_user
# from services.registration_service import process_registration
# from services.registration_service import TEMPLATE_REGISTRASI, parse_registration, save_registration
from services.chat_service import process_chat

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

    reply = process_chat(
        db=db,
        message=request.message,
        wa_id=request.wa_id,
        push_name=request.push_name
    )

    return {
        "reply": reply
    }