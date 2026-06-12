from fastapi import FastAPI

from database import engine
from models import Base

from routers.user import router as user_router
from routers.consultation import router as consultation_router
from routers.message import router as message_router
from routers.menu import router as menu_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(consultation_router)
app.include_router(message_router)
app.include_router(menu_router)