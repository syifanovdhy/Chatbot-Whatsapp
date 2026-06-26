from pydantic import BaseModel
from fastapi import APIRouter, Depends
from dependencies import get_db
from models import MenuLogDB, UserDB, ConsultationDB
from sqlalchemy.orm import Session
from routers import user
from services.menu_service import process_menu_choice, get_menu_name


router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    user_id: int

@router.post("/chat")
def chat(
    request: ChatRequest, 
    db: Session = Depends(get_db)
):
    menu_name = get_menu_name(request.message)
    if menu_name:
        log = MenuLogDB(
            user_id=request.user_id,
            menu=menu_name
        )
        db.add(log)
        db.commit()

    user = db.get(
    UserDB,
    request.user_id
)
    if not user:
        return {
            "reply": "User tidak ditemukan."
        }
    
    if request.message == "2":

        consultation = ConsultationDB(
            user_id=request.user_id,
            keperluan="Menunggu deskripsi",
            status="waiting_agent"
        )

        db.add(consultation)
        db.commit()

    reply = process_menu_choice(request.message)

    return {
        "reply": reply
    }