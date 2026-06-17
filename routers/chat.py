from pydantic import BaseModel
from fastapi import APIRouter, Depends
from dependencies import get_db
from models import MenuLogDB, UserDB
from sqlalchemy.orm import Session
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
    reply = process_menu_choice(request.message)

    return {
        "reply": reply
    }