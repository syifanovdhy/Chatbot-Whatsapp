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

    return None