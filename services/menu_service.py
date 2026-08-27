from sqlalchemy.orm import Session

from constants.states import (
    MAIN_MENU,
    PUBLICATION_MENU,
    DATA_MENU
)

from models import MenuLogDB, UserDB


def get_main_menu():
    return """
📋 *STATARA - Statistik Tanggap dan Ramah*

Silakan pilih layanan yang tersedia:

1️⃣ Publikasi
2️⃣ Konsultasi Statistik
3️⃣ Data Strategis
4️⃣ Pengaduan

Balas dengan angka 1-4.

Ketik *Menu* atau *0* untuk kembali ke menu utama.
Ketik *Selesai* untuk mengakhiri percakapan.
"""


def get_publication_menu():
    return """
📚 *Publikasi BPS Kabupaten Banggai Kepulauan*

Ketikkan kode publikasi yang ingin Anda akses.

Contoh:
DDA

Ketik *Pub* untuk kembali ke menu Publikasi.
Ketik *Menu* atau *0* untuk kembali ke menu utama.
Ketik *Selesai* untuk mengakhiri percakapan.
"""


def get_data_menu():
    return """
📊 *Data Strategis Kabupaten Banggai Kepulauan*

Ketikkan kode data yang ingin Anda ketahui.

D1. Kependudukan
D2. Kemiskinan
D3. PDRB
D4. Indeks Pembangunan Manusia (IPM)
D5. Ketenagakerjaan
D6. Geografis
Rincian. Untuk melihat rincian data yang tersedia.

Contoh:
Balas dengan *D1* untuk mengetahui data kependudukan.

Ketik *Data* untuk tetap di menu Data Strategis.
Ketik *Menu* atau *0* untuk kembali ke menu utama.
Ketik *Selesai* untuk mengakhiri percakapan.
"""


def get_complaint_menu():
    return """
📢 *Layanan Pengaduan*

Untuk menyampaikan pengaduan, silakan gunakan kanal resmi
SP4N-LAPOR!.

https://lapor.go.id

Ketik *Menu* atau *0* untuk kembali ke menu utama.
Ketik *Selesai* untuk mengakhiri percakapan.
"""


def handle_main_menu(
    db: Session,
    user: UserDB,
    message: str
):
    if user.registration_step != MAIN_MENU:
        return None

    message = message.strip()

    menu_name = get_menu_name(message)

    if menu_name:
        log = MenuLogDB(
            user_id=user.id,
            menu_type=menu_name
        )

        db.add(log)

    return process_menu_choice(
        db=db,
        user=user,
        choice=message
    )


def process_menu_choice(
    db: Session,
    user: UserDB,
    choice: str
):
    choice = choice.strip().lower()

    # ==========================================
    # Kembali ke menu utama
    # ==========================================
    if choice in ("0", "menu"):
        user.registration_step = MAIN_MENU
        db.commit()

        return get_main_menu()

    # ==========================================
    # 1. PUBLIKASI
    # ==========================================
    elif choice == "1":
        user.registration_step = PUBLICATION_MENU
        db.commit()

        return get_publication_menu()

    # ==========================================
    # 2. KONSULTASI
    # ==========================================
    elif choice == "2":
        # Tidak mengubah state di sini.
        # Consultation service akan menangani
        # pilihan menu 2.
        db.commit()

        return None

    # ==========================================
    # 3. DATA STRATEGIS
    # ==========================================
    elif choice == "3":
        user.registration_step = DATA_MENU
        db.commit()

        return get_data_menu()

    # ==========================================
    # 4. PENGADUAN
    # ==========================================
    elif choice == "4":
        db.commit()

        return get_complaint_menu()

    # ==========================================
    # Pilihan tidak tersedia
    # ==========================================
    return """
❌ *Pilihan menu tidak tersedia.*

Silakan pilih salah satu layanan:

1️⃣ Publikasi
2️⃣ Konsultasi Statistik
3️⃣ Data Strategis
4️⃣ Pengaduan

Balas dengan angka 1-4.

Ketik *Menu* atau *0* untuk kembali ke menu utama.
"""


MENU_MAPPING = {
    "1": "PUBLIKASI",
    "2": "KONSULTASI STATISTIK",
    "3": "DATA STRATEGIS",
    "4": "PENGADUAN"
}


def get_menu_name(choice: str):
    return MENU_MAPPING.get(
        choice.strip()
    )