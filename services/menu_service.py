from constants.states import MAIN_MENU
from models import UserDB


def handle_main_menu(user: UserDB, message: str):
    if user.registration_step != MAIN_MENU:
        return None
    return process_menu_choice(message)


def get_main_menu():
    return (
        "📋 *Silakan pilih layanan yang tersedia*\n\n"
        "1️⃣ Publikasi\n"
        "2️⃣ Konsultasi Statistik\n"
        "3️⃣ Data Strategis\n"
        "4️⃣ Pengaduan\n\n"
        "Balas dengan angka 1-4.\n\n"
        "Ketik *Selesai* untuk mengakhiri percakapan."
    )


def get_publication_menu():
    from services.publication_service import get_publication_menu as _get_publication_menu
    return _get_publication_menu()


def process_menu_choice(choice: str):
    choice = choice.strip().lower()

    if choice == "0" or choice == "menu":
        return get_main_menu()

    if choice == "1":
        return get_publication_menu()

    if choice == "2":
        return None

    if choice == "3":
        return (
            "📊 *Data Strategis Kabupaten Banggai Kepulauan*\n\n"
            "Fitur Data Strategis akan tersedia pada tahap berikutnya.\n\n"
            "Ketik *Menu* untuk kembali ke menu awal.\n"
            "Ketik *Selesai* untuk mengakhiri percakapan."
        )

    if choice == "4":
        return (
            "📢 *Layanan Pengaduan*\n\n"
            "Silakan menyampaikan pengaduan melalui kanal resmi SP4N-LAPOR!:\n"
            "https://lapor.go.id\n\n"
            "Ketik *Menu* untuk kembali ke menu awal.\n"
            "Ketik *Selesai* untuk mengakhiri percakapan."
        )

    return (
        "Menu tidak tersedia.\n\n"
        "Ketik *1-4* untuk memilih layanan atau *Menu* untuk kembali ke menu utama."
    )


MENU_MAPPING = {
    "1": "PUBLIKASI",
    "2": "KONSULTASI",
    "3": "DATA_STRATEGIS",
    "4": "PENGADUAN",
}


def get_menu_name(choice: str):
    return MENU_MAPPING.get(choice.strip())
