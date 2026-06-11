from pydantic import BaseModel


class UserCreate(BaseModel):
    nama: str
    email: str