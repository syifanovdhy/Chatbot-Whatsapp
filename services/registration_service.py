from sqlalchemy.orm import Session
from models import UserDB
from services.menu_service import get_main_menu

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

        if ":" not in line:
            continue

        key, value = line.split(":", 1)

        key = key.strip().lower()
        value = value.strip()

        if key == "nama":
            nama = value

        elif key == "instansi":
            instansi = value

        elif key == "email":
            email = value

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

def handle_registration(
    db: Session,
    user: UserDB,
    message: str
):

    print("=== HANDLE REGISTRATION ===")
    print("Step:", user.registration_step)
    print("Message:")
    print(message)

    if user.registration_step != "ASK_REGISTRATION":
        return None

    data = parse_registration(message)

    print("Parse Result:", data)

    if data is None:
        print("Gagal parse")
        return TEMPLATE_REGISTRASI

    print("Berhasil parse")

    save_registration(
        db=db,
        user=user,
        data=data
    )

    print("Step sesudah save:", user.registration_step)

    first_name = user.nama.split()[0]

    return (
        f"Terima kasih, Kak {first_name} 😊\n\n"
        "Registrasi berhasil.\n\n"
        + get_main_menu()
    )