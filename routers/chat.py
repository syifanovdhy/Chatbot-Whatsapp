from pydantic import BaseModel
from fastapi import APIRouter, Depends
from dependencies import get_db
from sqlalchemy.orm import Session
from services.chat_service import process_chat
from services.registration_service import parse_registration


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

@router.post("/test-parser")
def test_parser(request: ChatRequest):

    return parse_registration(request.message)