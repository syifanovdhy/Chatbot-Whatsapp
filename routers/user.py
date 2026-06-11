from fastapi import APIRouter, Depends
from sqlalchemy.orm import session

from dependencies import get_db
from models import UserDB
from schemas.user import UserCreate

router = APIRouter()


@router.post("/users-db")    
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

@router.get("/users-db")
def get_users_db(
    db: session = Depends(get_db)):
    users = db.query(UserDB).all()
    return users