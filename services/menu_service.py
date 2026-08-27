from constants.states import MAIN_MENU, PUBLICATION_MENU, DATA_MENU
from models import UserDB


def get_main_menu():
    return """📋 *STATARA - Statistik Tanggap dan Ramah*

Silakan pilih layanan yang tersedia:

1️⃣ Publikasi
2️⃣ Konsultasi Statistik
3️⃣ Data Strategis
4️⃣ Pengaduan

Balas dengan angka 1-4.

Ketik *Menu* atau *0* untuk kembali ke menu utama.
Ketik *Selesai* untuk mengakhiri percakapan."""


def get_publication_menu():
    return """📚 *PUBLIKASI BPS KABUPATEN BANGGAI KEPULAUAN*

Ketikkan kode publikasi yang ingin Anda akses.

Ketik *Pub* untuk menu Publikasi.
Ketik *Menu* untuk kembali ke menu awal.
Ketik *Selesai* untuk mengakhiri percakapan."""


def get_data_menu():
    return """📊 *DATA STRATEGIS KABUPATEN BANGGAI KEPULAUAN*

Ketikkan kode data yang ingin Anda ketahui.

D1. Kependudukan
D2. Kemiskinan
D3. PDRB
D4. Indeks Pembangunan Manusia (IPM)
D5. Ketenagakerjaan
D6. Geografis
Rincian. Untuk melihat rincian data yang tersedia.

Contoh: Balas dengan *D1* untuk mengetahui data kependudukan.

Ketik *Data* untuk tetap di menu Data Strategis.
Ketik *Menu* untuk kembali ke menu awal.
Ketik *Selesai* untuk mengakhiri percakapan."""


def handle_main_menu(user: UserDB, message: str):
    if user.registration_step != MAIN_MENU:
        return None
    return process_menu_choice(message)


def process_menu_choice(choice: str):
    choice = choice.strip().lower()

    if choice in ("0", "menu"):
        return get_main_menu()
    if choice == "1":
        return get_publication_menu()
    if choice == "2":
        return None
    if choice == "3":
        return get_data_menu()
    if choice == "4":
        return """📢 *LAYANAN PENGADUAN*

Silakan menyampaikan pengaduan melalui kanal pengaduan resmi SP4N-LAPOR!:
https://lapor.go.id

Ketik *Menu* atau *0* untuk kembali ke menu awal.
Ketik *Selesai* untuk mengakhiri percakapan."""

    return """Menu tidak tersedia.

Silakan pilih angka 1-4.
Ketik *Menu* atau *0* untuk melihat menu utama."""


MENU_MAPPING = {
    "1": "PUBLIKASI",
    "2": "KONSULTASI STATISTIK",
    "3": "DATA STRATEGIS",
    "4": "PENGADUAN",
}


def get_menu_name(choice: str):
    return MENU_MAPPING.get(choice.strip())
