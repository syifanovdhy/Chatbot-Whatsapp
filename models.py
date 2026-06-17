from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, DateTime
from datetime import datetime

class Base(DeclarativeBase):
    pass

class UserDB(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nama: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100))
    consultations: Mapped[list["ConsultationDB"]] = relationship(back_populates="user")
    menu_logs: Mapped[list["MenuLogDB"]] = relationship(back_populates="user")
    status: Mapped[str] = mapped_column(String(20), default="BOT_MODE")

class ConsultationDB(Base):
    __tablename__ = "consultations"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    keperluan: Mapped[str] = mapped_column(String(200))
    user: Mapped["UserDB"] = relationship(back_populates="consultations")
    status: Mapped[str] = mapped_column(String(50))
    messages: Mapped[list["MessageDB"]] = relationship(back_populates="consultation")
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    agent_replied: Mapped[bool] = mapped_column(default=False)
    timeout_sent : Mapped[bool] = mapped_column(default=False)

class MessageDB(Base) :    
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    consultation_id: Mapped[int] = mapped_column(ForeignKey("consultations.id"))
    sender: Mapped[str] = mapped_column(String(50))
    content: Mapped[str] = mapped_column(String(200))
    consultation : Mapped["ConsultationDB"] = relationship(back_populates="messages")

class MenuLogDB(Base):
    __tablename__ = "menu_logs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    menu_type: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user: Mapped["UserDB"] = relationship(back_populates="menu_logs")