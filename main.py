from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from enum import Enum
from database import engine
from models import Base, UserDB, ConsultationDB, MessageDB
import os
from sqlalchemy.orm import session
from dependencies import get_db
from routers.user import router as user_router
    
app = FastAPI()
app.include_router(user_router)
Base.metadata.create_all(bind=engine)

fake_users_db = []
next_user_id =1

fake_consultation_db = []
next_consultation_id = 1

fake_message_db = []
next_message_id = 1

fake_menu_logs_db = []
next_menu_log_id = 1

class UserCreate(BaseModel):
    nama: str
    email: str

class ConsultationCreate(BaseModel):
    user_id: int
    keperluan: str

class MessageCreate(BaseModel):
    consultation_id: int
    sender: str
    content: str

########

class Consultation(BaseModel):
    user_id: int
    keperluan: str

class User(BaseModel):
    nama: str
    email: str

class ConsultationStatus(Enum):
    MENUNGGU = "waiting_agent"
    DIPROSES = "active"
    SELESAI = "closed"

class SenderEnum(str, Enum):
    user = "user"
    agent = "agent"

class ConsultationStatus(BaseModel):
    status: ConsultationStatus

class Message(BaseModel):
    consultation_id: int
    sender: SenderEnum
    content: str

class MenuEnum(str, Enum):
    perpustakaan = "perpustakaan"
    konsultasi = "konsultasi"
    silastik = "silastik"
    romantik = "romantik"
    pengaduan = "pengaduan"

class MenuLog(BaseModel):
    user_id: int
    menu : MenuEnum

## Endpoint ##

@app.get("/debug-db")
def debug_db():
    return {
        "cwd": os.getcwd()
    }

@app.get("/")
def home():
    return {
        "message": "PST Bot Running"
    }

@app.post("/users-db")    
def create_user_db(
    user: UserCreate, 
    db: session = Depends(get_db)
    ):

    new_user = UserDB(
        nama=user.nama, 
        email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "id": new_user.id,
        "nama": new_user.nama,
        "email": new_user.email
    }

@app.get("/users-db")
def get_users_db(
    db: session = Depends(get_db)):
    users = db.query(UserDB).all()
    return users

@app.get("/tables-test")
def tables_test():
    return {"message": "Tables initialized"}

@app.post("/consultations-db")
def create_consultation_db(
    consultation: ConsultationCreate,
    db: session = Depends(get_db)
):
    new_consultation = ConsultationDB(
        user_id=consultation.user_id,
        keperluan=consultation.keperluan,
        status="waiting_agent"
    )
    db.add(new_consultation)
    db.commit()
    db.refresh(new_consultation)
    return new_consultation

@app.get("/consultations-db")
def get_consultations_db(
    db: session = Depends(get_db)
):
    consultations = db.query(ConsultationDB).all()
    return consultations

@app.post("/messages-db")
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

@app.get("/messages-db")
def get_messages_db(
    db: session = Depends(get_db)
):
    messages = db.query(MessageDB).all()
    return messages

@app.get("/consultations-db/{consultation_id}/messages")
def get_consultation_messages_db(
    consultation_id: int,
    db: session = Depends(get_db)
):
    messages = db.query(MessageDB).filter(
        MessageDB.consultation_id == consultation_id).all()
    return messages

@app.get("/test-relation/{consultation_id}")
def test_relation(
    consultation_id: int, db: 
    session = Depends(get_db)):
    
    consultation = db.query(
        ConsultationDB
        ).filter(
            ConsultationDB.id == consultation_id
            ).first()
    if not consultation:
        raise HTTPException(status_code=404, detail="Consultation not found")
    return {
        "consultation.id": consultation.id,
        "jumlah_pesan": len(consultation.messages)
    }

# Endpoint  Fake Database #

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

    user_found = False

    for user in fake_users_db:
        if user["id"] == consultation.user_id:
            user_found = True
            break

    if not user_found:
        raise HTTPException(
            status_code=404, 
            detail="User not found")

    global next_consultation_id

    new_consultation = {
        "id": next_consultation_id,
        "user_id": consultation.user_id,
        "keperluan": consultation.keperluan,
        "status": "waiting_agent"
    }

    fake_consultation_db.append(new_consultation)
    next_consultation_id += 1

    return new_consultation

@app.get("/consultations")
def get_consultations():
    return fake_consultation_db

@app.put("/consultations/{consultation_id}/status")
def update_consultation_status(
    consultation_id: int, 
    status_data: ConsultationStatus):
    for consultation in fake_consultation_db:
        if consultation["id"] == consultation_id:
            consultation["status"] = status_data.status
            return consultation
    raise HTTPException(
        status_code=404, detail="Consultation not found")

@app.post("/messages")
def create_message(message: Message):
    global next_message_id

    new_message = {
        "id": next_message_id,
        "consultation_id": message.consultation_id,
        "sender": message.sender,
        "content": message.content
    }

    fake_message_db.append(new_message)
    next_message_id += 1

    return new_message

@app.get("/messages")
def get_messages():
    return fake_message_db

@app.get("/consultations/{consultation_id}/messages")
def get_consultation_messages(consultation_id: int):
    
    consultation_messages = []
    for message in fake_message_db:
        if message["consultation_id"] == consultation_id:
            consultation_messages.append(message)
    return consultation_messages

@app.post("/menu-logs")
def create_menu_log(menu_log: MenuLog):
    user_found = False

    for user in fake_users_db:
        if user["id"] == menu_log.user_id:
            user_found = True
            break

    if not user_found:
        raise HTTPException(
            status_code=404, 
            detail="User not found")
    
    global next_menu_log_id

    new_log = {
        "id": next_menu_log_id,
        "user_id": menu_log.user_id,
        "menu": menu_log.menu
    }

    fake_menu_logs_db.append(new_log)
    next_menu_log_id +=1
    return new_log

@app.get("/menu-logs")
def get_menu_logs():
    return fake_menu_logs_db

@app.get("/stats")
def get_stats ():
    unique_users = len(fake_users_db)
    total_consultations = len(fake_consultation_db)
    total_message = len(fake_message_db)
    menu_stats = {}

    for log in fake_menu_logs_db:
        menu=log["menu"]

        if menu not in menu_stats:
            menu_stats[menu]=0

        menu_stats[menu] +=1
    
    return {
        "unique_users": unique_users,
        "total_consultations": total_consultations,
        "total_messages": total_message,
        "menu_stats": menu_stats
    }
