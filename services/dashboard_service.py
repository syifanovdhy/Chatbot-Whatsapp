from sqlalchemy import func
from sqlalchemy.orm import Session
from models import ConsultationDB, MenuLogDB, MessageDB, UserDB
from constants.states import CONSULTATION_WAITING,CONSULTATION_ACTIVE
from datetime import datetime, timedelta
from constants.dashboard import PERIOD_ALL, PERIOD_TODAY, PERIOD_WEEK, PERIOD_MONTH

SERVICE_ORDER = [
    ("PUBLIKASI", "📚 Publikasi"),
    ("KONSULTASI", "📞 Konsultasi Statistik"),
    ("DATA_STRATEGIS", "📊 Data Strategis"),
    ("PENGADUAN", "📢 Pengaduan")
]

def get_period_start(
    period: str
):

    now = datetime.utcnow()

    if period == PERIOD_TODAY:

        return datetime(
            now.year,
            now.month,
            now.day
        )

    if period == PERIOD_WEEK:

        return (
            datetime(
                now.year,
                now.month,
                now.day
            )
            - timedelta(days=now.weekday())
        )

    if period == PERIOD_MONTH:

        return datetime(
            now.year,
            now.month,
            1
        )

    return None

def get_service_statistics(
    db: Session,
    period: str = "all"
):

    query = db.query(
        MenuLogDB.menu_type,
        func.count(MenuLogDB.id).label("jumlah")
    )

    period_start = get_period_start(period)

    if period_start is not None:

        query = query.filter(
            MenuLogDB.created_at >= period_start
        )

    result = (
        query
        .group_by(MenuLogDB.menu_type)
        .all()
    )

    counts = {
        menu: jumlah
        for menu, jumlah in result
    }

    return [
        {
            "menu": menu_name,
            "kode": menu_code,
            "jumlah": counts.get(
                menu_code,
                0
            )
        }
        for menu_code, menu_name in SERVICE_ORDER
    ]

def get_dashboard_summary(
    db: Session,
    period: str = "all"
):
    period_start = get_period_start(period)

    service_query = db.query(MenuLogDB)

    if period_start is not None:
        service_query = service_query.filter(
            MenuLogDB.created_at >= period_start
        )

    total_services = service_query.count()

    user_ids = (
        service_query
        .with_entities(MenuLogDB.user_id)
        .distinct()
        .all()
    )

    total_users = len(user_ids)

    return {
        "total_users": total_users,
        "total_services": total_services
    }

def get_active_consultations(db: Session):
    consultations = (
        db.query(ConsultationDB)
        .filter(
            ConsultationDB.status.in_([
                CONSULTATION_WAITING,
                CONSULTATION_ACTIVE,
            ])
        )
        .order_by(ConsultationDB.started_at.desc())
        .all()
    )

    result = []
    for consultation in consultations:
        whatsapp_account = next(iter(consultation.user.whatsapp_accounts), None)
        last_message = (
            db.query(MessageDB)
            .filter(MessageDB.consultation_id == consultation.id)
            .order_by(MessageDB.created_at.desc())
            .first()
        )
        result.append({
            "id": consultation.id,
            "nama": consultation.user.nama or "Pengguna WhatsApp",
            "wa_id": whatsapp_account.wa_id if whatsapp_account else "-",
            "keperluan": consultation.keperluan,
            "status": consultation.status,
            "agent_replied": consultation.agent_replied,
            "started_at": consultation.started_at.isoformat(),
            "last_message": last_message.content if last_message else "-",
        })

    return result

def get_daily_service_statistics(
    db: Session,
    period: str = "month"
):
    period_start = get_period_start(period)

    query = db.query(
        func.date(MenuLogDB.created_at).label("tanggal"),
        func.count(MenuLogDB.id).label("jumlah")
    )

    if period_start is not None:
        query = query.filter(
            MenuLogDB.created_at >= period_start
        )

    result = (
        query
        .group_by(
            func.date(MenuLogDB.created_at)
        )
        .order_by(
            func.date(MenuLogDB.created_at)
        )
        .all()
    )

    return [
        {
            "tanggal": str(tanggal),
            "jumlah": jumlah
        }
        for tanggal, jumlah in result
    ]

def get_daily_service_breakdown(
    db: Session,
    period: str = "month"
):
    period_start = get_period_start(period)

    query = db.query(
        func.date(MenuLogDB.created_at).label("tanggal"),
        MenuLogDB.menu_type,
        func.count(MenuLogDB.id).label("jumlah")
    )

    if period_start is not None:
        query = query.filter(
            MenuLogDB.created_at >= period_start
        )

    result = (
        query
        .group_by(
            func.date(MenuLogDB.created_at),
            MenuLogDB.menu_type
        )
        .order_by(
            func.date(MenuLogDB.created_at)
        )
        .all()
    )

    return [
        {
            "tanggal": str(tanggal),
            "menu": menu,
            "jumlah": jumlah
        }
        for tanggal, menu, jumlah in result
    ]

