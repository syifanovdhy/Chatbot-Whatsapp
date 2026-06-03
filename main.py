from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
class User(BaseModel):
    nama: str
    instansi: str
    email: str
    nomor_wa: str

@app.get("/")
def home():
    return {
        "message": "PST Bot Running"
    }
    

@app.post("/users")
def create_user(user: User):
    return {
        "nama": user.nama,
        "email": user.email
    }

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {
        "user_id": user_id,
        "nama": "Altair"
    }