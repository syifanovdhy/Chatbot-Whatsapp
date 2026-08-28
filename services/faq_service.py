from sqlalchemy.orm import Session

from constants.states import FAQ_MENU
from models import UserDB


FAQ_DATA = {
    "1": {
        "question": "Apa itu STATARA?",
        "answer": (
            "STATARA (Statistik Tanggap dan Ramah) merupakan layanan "
            "chatbot WhatsApp BPS Kabupaten Banggai Kepulauan yang membantu "
            "pengguna memperoleh publikasi, data strategis, konsultasi "
            "statistik, dan informasi pengaduan."
        ),
    },

    "2": {
        "question": "Apa saja layanan yang tersedia di STATARA?",
        "answer": (
            "STATARA menyediakan 4 layanan utama:\n\n"
            "1️⃣ Publikasi\n"
            "2️⃣ Konsultasi Statistik\n"
            "3️⃣ Data Strategis\n"
            "4️⃣ Pengaduan"
        ),
    },

    "3": {
        "question": "Bagaimana cara mendapatkan publikasi BPS?",
        "answer": (
            "Anda dapat memperoleh publikasi BPS Kabupaten Banggai "
            "Kepulauan melalui menu *Publikasi*.\n\n"
            "Silakan kembali ke menu utama dan pilih *1. Publikasi*."
        ),
    },

    "4": {
        "question": "Bagaimana cara mendapatkan data statistik?",
        "answer": (
            "Anda dapat melihat beberapa data strategis Kabupaten "
            "Banggai Kepulauan melalui menu *Data Strategis*.\n\n"
            "Silakan kembali ke menu utama dan pilih "
            "*3. Data Strategis*."
        ),
    },

    "5": {
        "question": "Bagaimana cara melakukan konsultasi statistik?",
        "answer": (
            "Untuk melakukan konsultasi statistik, silakan kembali "
            "ke menu utama kemudian pilih *2. Konsultasi Statistik*.\n\n"
            "Pertanyaan Anda akan diteruskan kepada petugas PST "
            "BPS Kabupaten Banggai Kepulauan."
        ),
    },

    "6": {
        "question": "Apakah konsultasi statistik dikenakan biaya?",
        "answer": (
            "Layanan konsultasi statistik melalui PST BPS Kabupaten "
            "Banggai Kepulauan tidak dipungut biaya."
        ),
    },

    "7": {
        "question": "Bagaimana cara menyampaikan pengaduan?",
        "answer": (
            "Pengaduan dapat disampaikan melalui kanal resmi "
            "SP4N-LAPOR!.\n\n"
            "Silakan pilih menu *4. Pengaduan* untuk mendapatkan "
            "informasi dan tautan pengaduan."
        ),
    },

    "8": {
        "question": "Bagaimana cara kembali ke menu utama?",
        "answer": (
            "Ketik *Menu* atau *0* untuk kembali ke menu utama."
        ),
    },
}


def get_faq_menu():
    return """
❓ *FAQ STATARA*

Berikut pertanyaan yang sering ditanyakan:

1️⃣ Apa itu STATARA?
2️⃣ Apa saja layanan yang tersedia?
3️⃣ Bagaimana cara mendapatkan publikasi BPS?
4️⃣ Bagaimana cara mendapatkan data statistik?
5️⃣ Bagaimana cara melakukan konsultasi statistik?
6️⃣ Apakah konsultasi statistik dikenakan biaya?
7️⃣ Bagaimana cara menyampaikan pengaduan?
8️⃣ Bagaimana cara kembali ke menu utama?

Balas dengan angka 1-8.

Ketik *FAQ* untuk menampilkan kembali daftar pertanyaan.
Ketik *Menu* atau *0* untuk kembali ke menu utama.
Ketik *Selesai* untuk mengakhiri percakapan.
"""


def get_faq_detail(choice: str):
    choice = choice.strip()

    if choice not in FAQ_DATA:
        return None

    faq = FAQ_DATA.get(choice)

    return f"""
❓ *FAQ STATARA*

*{faq['question']}*

{faq['answer']}

Ketik *FAQ* untuk kembali ke daftar pertanyaan.
Ketik *Menu* atau *0* untuk kembali ke menu utama.
Ketik *Selesai* untuk mengakhiri percakapan.
"""


def handle_faq(
    db: Session,
    user: UserDB,
    message: str
):
    if user.registration_step != FAQ_MENU:
        return None

    message = message.strip()

    if message.lower() == "faq":
        return get_faq_menu()

    return get_faq_detail(message)