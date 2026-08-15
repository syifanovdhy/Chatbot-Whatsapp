import csv
import datetime

from constants.dashboard import PERIOD_MONTH, PERIOD_TODAY, PERIOD_WEEK
from services.dashboard_service import (
    get_daily_service_breakdown,
    get_period_start
)
from models import MenuLogDB

SERVICE_ORDER = [
    ("PERPUSTAKAAN", "Perpustakaan"),
    ("KONSULTASI", "Konsultasi Statistik"),
    ("SILASTIK", "Silastik"),
    ("ROMANTIK", "Romantik"),
    ("PENGADUAN", "Pengaduan"),
]


def create_service_export(
    db,
    period: str,
    output_path: str
):

    data = get_daily_service_breakdown(
        db=db,
        period=period
    )

    rows_by_date = {}

    for item in data:

        tanggal = item["tanggal"]

        if tanggal not in rows_by_date:
            rows_by_date[tanggal] = {
                code: 0
                for code, _ in SERVICE_ORDER
            }

        if item["menu"] in rows_by_date[tanggal]:
            rows_by_date[tanggal][
                item["menu"]
            ] = item["jumlah"]

    headers = [
        "Tanggal",
        "Perpustakaan",
        "Konsultasi Statistik",
        "Silastik",
        "Romantik",
        "Pengaduan",
        "Total"
    ]

    with open(
        output_path,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        writer = csv.writer(file)

        writer.writerow(headers)

        for tanggal in sorted(rows_by_date):

            values = rows_by_date[tanggal]

            total = sum(values.values())

            writer.writerow([
                tanggal,
                values["PERPUSTAKAAN"],
                values["KONSULTASI"],
                values["SILASTIK"],
                values["ROMANTIK"],
                values["PENGADUAN"],
                total
            ])

def get_period_start(period: str):

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
            - datetime.timedelta(days=now.weekday())
        )

    if period == PERIOD_MONTH:
        return datetime(
            now.year,
            now.month,
            1
        )

    return None