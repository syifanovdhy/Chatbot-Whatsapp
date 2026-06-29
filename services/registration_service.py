from sqlalchemy.orm import Session
from models import UserDB


def process_registration(
    db: Session,
    user: UserDB,
    message: str
):
    """
    Mengolah proses registrasi pengguna.
    Return:
        - None jika registrasi belum selesai
        - String balasan chatbot
    """

    if user.registration_step == "ASK_NAME":

        user.nama = message.strip()

        user.registration_step = "ASK_INSTITUTION"

        db.commit()

        first_name = user.nama.split()[0]

        return (
            f"Terima kasih, Kak {first_name} 😊\n\n"
            "Sekarang boleh tahu berasal dari instansi mana?"
        )
    
    if user.registration_step == "ASK_INSTITUTION":

        user.instansi = message.strip()

        user.registration_step = "ASK_EMAIL"

        db.commit()

        return (
            "Terima kasih 😊\n\n"
            "Sekarang silakan masukkan alamat email.\n\n"
            "Jika tidak ingin mengisi, ketik tanda -"
        )
    
    if user.registration_step == "ASK_EMAIL":

        if message.strip() == "-":
            user.email = ""
        else:
            user.email = message.strip()

        user.registration_step = "MAIN_MENU"

        db.commit()

        first_name = user.nama.split()[0]

        return (
            f"Registrasi selesai, Kak {first_name}! 🎉\n\n"
            "Silakan pilih layanan berikut:\n\n"
            "1. Perpustakaan\n"
            "2. Konsultasi Statistik\n"
            "3. Penjualan Produk Statistik (Silastik)\n"
            "4. Rekomendasi Statistik (Romantik)\n"
            "5. Pengaduan\n"
        )

    return None