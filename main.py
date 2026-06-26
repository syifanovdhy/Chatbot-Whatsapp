from fastapi import FastAPI

from database import engine
from models import Base

from routers.user import router as user_router
from routers.consultation import router as consultation_router
from routers.message import router as message_router
from routers.menu import router as menu_router
from routers.stats import router as stats_router
from routers.agent import router as agent_router
from routers.chat import router as agent_chat

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(consultation_router)
app.include_router(message_router)
app.include_router(menu_router)
app.include_router(stats_router)
app.include_router(agent_router)
app.include_router(agent_chat)