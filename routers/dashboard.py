from pydantic import BaseModel
import os
from datetime import datetime

from fastapi import APIRouter, Depends, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from starlette.background import BackgroundTask

from dependencies import get_db

from services.dashboard_service import (
    get_dashboard_summary,
    get_service_statistics,
    get_daily_service_statistics
)

from services.dashboard_export_service import (
    create_service_export
)

class ReplyRequest(BaseModel):
    message: str

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

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


