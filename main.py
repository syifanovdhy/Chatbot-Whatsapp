from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

fake_users_db = []
next_user_id =1

fake_consultation_db = []
next_consultation_id = 1

class Consultation(BaseModel):
    user_id: int
    keperluan: str

class User(BaseModel):
    nama: str
    email: str

@app.get("/")
def home():
    return {
        "message": "PST Bot Running"
    }
    

@app.post("/users")
def create_user(user: User):

    global next_user_id

    new_user = {
        "id": next_user_id,
        "nama": user.nama,
        "email": user.email
    }


    fake_users_db.append(new_user)
    next_user_id += 1

    return {
        "message": "User berhasil ditambahkan"
    }

@app.get("/users")
def get_users():
    return fake_users_db

@app.get("/users/{user_id}")
def get_user(user_id: int):
    for user in fake_users_db:
        if user["id"] == user_id:
            return user
    return {"message": "User not found"}

@app.post("/consultations")
def create_consultation(consultation: Consultation):

    global next_consultation_id

    new_consultation = {
        "id": next_consultation_id,
        "user_id": consultation.user_id,
        "keperluan": consultation.keperluan,
        "status": "menunggu"
    }

    fake_consultation_db.append(new_consultation)
    next_consultation_id += 1

    return new_consultation

@app.get("/consultations")
def get_consultations():
    return fake_consultation_db