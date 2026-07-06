from sqlalchemy.orm import Session
from models import UserDB

TEMPLATE_REGISTRASI = (
    "👋 Selamat datang di Pelayanan Statistik Terpadu (PST)\n"
    "BPS Kabupaten Banggai Kepulauan.\n\n"
    "Sebelum menggunakan layanan, mohon lengkapi data berikut "
    "dalam *satu pesan*.\n\n"
    "Format:\n\n"
    "Nama: ...\n"
    "Instansi: ...\n"
    "Email: ... (isi '-' jika tidak ada)\n\n"
    "Contoh:\n"
    "Nama: Syifa Novdhy\n"
    "Instansi: Universitas Hasanuddin\n"
    "Email: -"
)


def parse_registration(message: str):

    nama = None
    instansi = None
    email = None

    lines = message.splitlines()

    for line in lines:

        line = line.strip()

        if line.lower().startswith("nama:"):
            nama = line.split(":", 1)[1].strip()

        elif line.lower().startswith("instansi:"):
            instansi = line.split(":", 1)[1].strip()

        elif line.lower().startswith("email:"):
            email = line.split(":", 1)[1].strip()

    if not nama or not instansi or email is None:
        return None

    return {
        "nama": nama,
        "instansi": instansi,
        "email": email
    }


def save_registration(
    db: Session,
    user: UserDB,
    data: dict
):

    user.nama = data["nama"]
    user.instansi = data["instansi"]

    if data["email"] == "-":
        user.email = ""
    else:
        user.email = data["email"]

    user.registration_step = "MAIN_MENU"

    db.commit()