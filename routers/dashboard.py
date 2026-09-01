from pydantic import BaseModel
import os
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from starlette.background import BackgroundTask

from dependencies import get_db
from constants.states import CONSULTATION_ACTIVE, CONSULTATION_WAITING
from models import ConsultationDB

from services.dashboard_service import (
    get_dashboard_summary,
    get_active_consultations,
    get_service_statistics,
    get_daily_service_statistics
)
from services.consultation_service import finish_consultation
from services.whatsapp_gateway import send_whatsapp_message

from services.dashboard_export_service import (
    create_service_export
)

class ReplyRequest(BaseModel):
    message: str

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/consultations/active")
def active_consultations(db: Session = Depends(get_db)):
    return get_active_consultations(db=db)

@router.post("/consultations/{consultation_id}/finish")
def finish_dashboard_consultation(
    consultation_id: int,
    db: Session = Depends(get_db),
):
    consultation = db.get(ConsultationDB, consultation_id)
    if consultation is None:
        raise HTTPException(status_code=404, detail="Konsultasi tidak ditemukan")

    if consultation.status not in [CONSULTATION_WAITING, CONSULTATION_ACTIVE]:
        raise HTTPException(status_code=409, detail="Konsultasi sudah tidak aktif")

    finish_consultation(db=db, consultation=consultation)

    notification_sent = False
    if consultation.user.whatsapp_accounts:
        try:
            send_whatsapp_message(
                consultation.user.whatsapp_accounts[0].wa_id,
                (
                    "Konsultasi telah selesai.\n\n"
                    "Terima kasih telah menggunakan Pelayanan Statistik Terpadu "
                    "BPS Kabupaten Banggai Kepulauan.\n\n"
                    "Ketik *Menu* atau *0* untuk kembali ke menu utama."
                ),
            )
            notification_sent = True
        except Exception:
            notification_sent = False

    return {
        "message": "Konsultasi telah selesai",
        "notification_sent": notification_sent,
    }

@router.get("/statistics")
def dashboard_statistics(
    period: str = Query(
        "all",
        pattern="^(all|today|week|month)$"
    ),
    db: Session = Depends(get_db)
):

    return get_service_statistics(
        db=db,
        period=period
    )

@router.get("/summary")
def dashboard_summary(
    period: str = Query(
        "all",
        pattern="^(all|today|week|month)$"
    ),
    db: Session = Depends(get_db)
):

    return get_dashboard_summary(
        db=db,
        period=period
    )

@router.get("/daily-statistics")
def dashboard_daily_statistics(
    period: str = Query(
        "month",
        pattern="^(all|today|week|month)$"
    ),
    db: Session = Depends(get_db)
):

    return get_daily_service_statistics(
        db=db,
        period=period
    )

@router.get("/export")
def export_service_report(
    period: str = Query(
        "month",
        pattern="^(all|today|week|month)$"
    ),
    db: Session = Depends(get_db)
):

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    filename = (
        f"rekap_layanan_{period}_"
        f"{timestamp}.csv"
    )

    output_path = os.path.join(
        "temp",
        filename
    )

    os.makedirs(
        "temp",
        exist_ok=True
    )

    create_service_export(
        db=db,
        period=period,
        output_path=output_path
    )

    return FileResponse(
        path=output_path,
        filename=filename,
        media_type=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
        background=BackgroundTask(
            os.remove,
            output_path
        )
    )


