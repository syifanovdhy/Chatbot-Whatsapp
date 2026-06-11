from fastapi import APIRouter, Depends
from sqlalchemy.orm import session

from dependencies import get_db
from models import MessageDB
from schemas.message import MessageCreate

router = APIRouter()

@router.post("/messages-db")
def create_message_db(
    message: MessageCreate,
    db: session = Depends(get_db)
):
    new_message = MessageDB(
        consultation_id=message.consultation_id,
        sender=message.sender,
        content=message.content
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message

@router.get("/messages-db")
def get_messages_db(
    db: session = Depends(get_db)
):
    messages = db.query(MessageDB).all()
    return messages
