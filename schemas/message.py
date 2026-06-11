from pydantic import BaseModel

class MessageCreate(BaseModel):
    consultation_id: int
    sender: str
    content: str