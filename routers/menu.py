from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies import get_db
from models import MenuLogDB
from schemas.menu_log import MenuLogCreate

router = APIRouter()


@router.post("/menu-logs/")
def create_menu_log(
    menu_log: MenuLogCreate, 
    db: Session = Depends(get_db)):

    new_log = MenuLogDB(
    user_id=menu_log.user_id,
    menu_type=menu_log.menu_type.value
    )
    
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log

@router.get("/menu-logs")
def get_menu_logs(
    db:Session = Depends(get_db)
):
    return db.query(MenuLogDB).all()