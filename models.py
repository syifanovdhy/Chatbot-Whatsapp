from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

class Base(DeclarativeBase):
    pass

class UserDB(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nama: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100))

class ConsultationDB(Base):
    __tablename__ = "consultations"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    keperluan: Mapped[str] = mapped_column(String(200))
    status: Mapped[str] = mapped_column(String(50))

class MessageDB(Base) :    
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    consultation_id: Mapped[int] = mapped_column(ForeignKey("consultations.id"))
    sender: Mapped[str] = mapped_column(String(50))
    content: Mapped[str] = mapped_column(String(200))