from sqlalchemy.orm import Session

from constants.states import PUBLICATION_MENU
from models import UserDB


PUBLICATIONS = {
    "DDA": "Kabupaten Banggai Kepulauan Dalam Angka",
    "PDRBL": (
        "Produk Domestik Regional Bruto Kabupaten Banggai Kepulauan "
        "Menurut Lapangan Usaha"
    ),
    "PDRBP": (
        "Produk Domestik Regional Bruto Kabupaten Banggai Kepulauan "
        "Menurut Pengeluaran"
    ),
    "STATKESRA": "Statistik Kesejahteraan Rakyat",
    "SKD": (
        "Analisis Hasil Survei Kebutuhan Data "
        "BPS Kabupaten Banggai Kepulauan"
    ),
    "KCA30": "Kecamatan Totikum Dalam Angka",
    "KCA31": "Kecamatan Totikum Selatan Dalam Angka",
    "KCA40": "Kecamatan Tinangkung Dalam Angka",
    "KCA41": "Kecamatan Tinangkung Selatan Dalam Angka",
    "KCA42": "Kecamatan Tinangkung Utara Dalam Angka",
    "KCA50": "Kecamatan Liang Dalam Angka",
    "KCA51": "Kecamatan Peling Tengah Dalam Angka",
    "KCA60": "Kecamatan Bulagi Dalam Angka",
    "KCA61": "Kecamatan Bulagi Selatan Dalam Angka",
    "KCA62": "Kecamatan Bulagi Utara Dalam Angka",
    "KCA70": "Kecamatan Buko Dalam Angka",
    "KCA71": "Kecamatan Buko Selatan Dalam Angka",
}


def get_publication_menu():
    return """
📚 *Publikasi BPS Kabupaten Banggai Kepulauan*

Ketikkan Kode Publikasi yang ingin anda akses.

DDA. Kabupaten Banggai Kepulauan Dalam Angka
PDRBL. Produk Domestik Regional Bruto Kabupaten Banggai Kepulauan Menurut Lapangan Usaha
PDRBP. Produk Domestik Regional Bruto Kabupaten Banggai Kepulauan Menurut Pengeluaran
Statkesra. Statistik Kesejahteraan Rakyat
SKD. Analisis Hasil Survei Kebutuhan Data BPS Kabupaten Banggai Kepulauan
KCA30. Kecamatan Totikum Dalam Angka
KCA31. Kecamatan Totikum Selatan Dalam Angka
KCA40. Kecamatan Tinangkung Dalam Angka
KCA41. Kecamatan Tinangkung Selatan Dalam Angka
KCA42. Kecamatan Tinangkung Utara Dalam Angka
KCA50. Kecamatan Liang Dalam Angka
KCA51. Kecamatan Peling Tengah Dalam Angka
KCA60. Kecamatan Bulagi Dalam Angka
KCA61. Kecamatan Bulagi Selatan Dalam Angka
KCA62. Kecamatan Bulagi Utara Dalam Angka
KCA70. Kecamatan Buko Dalam Angka
KCA71. Kecamatan Buko Selatan Dalam Angka

Ketik *Menu* untuk kembali ke menu awal.
Ketik *Selesai* untuk mengakhiri percakapan.
"""


def get_dda_detail():
    return """
📖 *Kabupaten Banggai Kepulauan Dalam Angka*

Tahun 2023
s.bps.go.id/dda7201_2023

Tahun 2022
s.bps.go.id/dda7201_2022

Untuk publikasi selengkapnya dapat mengunjungi:
https://bangkepkab.bps.go.id/publication.html

Ketik *Pub* untuk kembali ke menu Publikasi BPS Kabupaten Banggai Kepulauan
Ketik *Menu* untuk kembali ke menu awal.
Ketik *Selesai* untuk mengakhiri percakapan.
"""


def get_publication_detail(code: str):
    code = code.strip().upper()

    if code not in PUBLICATIONS:
        return None

    if code == "DDA":
        return get_dda_detail()

    return f"""
📖 *{PUBLICATIONS[code]}*

Informasi lengkap publikasi ini dapat diakses melalui:
https://bangkepkab.bps.go.id/publication.html

Ketik *Pub* untuk kembali ke menu Publikasi BPS Kabupaten Banggai Kepulauan
Ketik *Menu* untuk kembali ke menu awal.
Ketik *Selesai* untuk mengakhiri percakapan.
"""


def handle_publication(
    db: Session,
    user: UserDB,
    message: str
):
    if user.registration_step != PUBLICATION_MENU:
        return None

    message = message.strip()

    # ==========================================
    # KEMBALI KE MENU PUBLIKASI
    # ==========================================
    if message.lower() == "pub":
        return get_publication_menu()

    # ==========================================
    # DETAIL PUBLIKASI
    # ==========================================
    detail = get_publication_detail(message)

    if detail:
        return detail

    # ==========================================
    # KODE TIDAK DITEMUKAN
    # ==========================================
    return f"""
❌ Kode publikasi *{message}* tidak ditemukan.

Silakan pilih kode publikasi yang tersedia.

{get_publication_menu()}
"""