from pydantic import BaseModel

class ChatRequest(BaseModel):
    wa_id: str
    push_name: str = ""
    message: str
    