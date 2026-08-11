from sqlalchemy.orm import Session

from constants.states import MAIN_MENU
from models import MenuLogDB, UserDB

def handle_main_menu(
    db: Session,
    user: UserDB,
    message: str
):

    if user.registration_step != MAIN_MENU:
        return None

    menu_name = get_menu_name(message)

    if menu_name:

        log = MenuLogDB(
            user_id=user.id,
            menu_type=menu_name
        )

        db.add(log)
        db.commit()

    return process_menu_choice(message)

def get_main_menu():
    return """
    📋 *Silakan pilih layanan yang tersedia*

    1️⃣ Perpustakaan
    2️⃣ Konsultasi
    3️⃣ Silastik
    4️⃣ Romantik
    5️⃣ Pengaduan

    Balas dengan angka 1-5.
    """

def process_menu_choice(choice: str):
    if choice == "0":
        return get_main_menu()

    elif choice == "1":
        return """
        📚 PERPUSTAKAAN

        Silakan kunjungi:

        https://bangkepkab.bps.go.id

        Ketik 0 untuk kembali ke menu utama.
        """
    elif choice == "2":
        return None 

    elif choice == "3":
        return """
        🛒 SILASTIK

        https://silastik.bps.go.id

        Ketik 0 untuk kembali ke menu utama.
        """

    elif choice == "4":
        return """
        📋 ROMANTIK

        https://romantik.web.bps.go.id

        Ketik 0 untuk kembali ke menu utama.
        """

    elif choice == "5":
        return """
        📢 SP4N LAPOR

        https://lapor.go.id

        Ketik 0 untuk kembali ke menu utama.
        """

    return """
    Menu tidak tersedia.

    Ketik 0 untuk melihat menu utama.
    """   

MENU_MAPPING = {
    "1": "PERPUSTAKAAN",
    "2": "KONSULTASI",
    "3": "SILASTIK",
    "4": "ROMANTIK",
    "5": "PENGADUAN"
}

def get_menu_name(choice: str):
    return MENU_MAPPING.get(choice)
