from pydantic import BaseModel
from fastapi import APIRouter
from services.menu_services import process_menu_choice

router = APIRouter()
class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
def chat(
    request: ChatRequest
):
    
    reply = process_menu_choice(
    request.message
    )

    return {
        "reply": reply
    }