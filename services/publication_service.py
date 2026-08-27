from constants.states import MAIN_MENU, PUBLICATION_MENU
from models import UserDB


PUBLICATIONS = {
    "DDA": {
        "name": "Kabupaten Banggai Kepulauan Dalam Angka",
        "years": {
            "2023": "s.bps.go.id/dda7201_2023",
            "2022": "s.bps.go.id/dda7201_2022",
        },
    },
    "PDRBL": {
        "name": "Produk Domestik Regional Bruto Kabupaten Banggai Kepulauan Menurut Lapangan Usaha",
    },
    "PDRBP": {
        "name": "Produk Domestik Regional Bruto Kabupaten Banggai Kepulauan Menurut Pengeluaran",
    },
    "STATKESRA": {
        "name": "Statistik Kesejahteraan Rakyat",
    },
    "SKD": {
        "name": "Analisis Hasil Survei Kebutuhan Data BPS Kabupaten Banggai Kepulauan",
    },
    "KCA30": {"name": "Kecamatan Totikum Dalam Angka"},
    "KCA31": {"name": "Kecamatan Totikum Selatan Dalam Angka"},
    "KCA40": {"name": "Kecamatan Tinangkung Dalam Angka"},
    "KCA41": {"name": "Kecamatan Tinangkung Selatan Dalam Angka"},
    "KCA42": {"name": "Kecamatan Tinangkung Utara Dalam Angka"},
    "KCA50": {"name": "Kecamatan Liang Dalam Angka"},
    "KCA51": {"name": "Kecamatan Peling Tengah Dalam Angka"},
    "KCA60": {"name": "Kecamatan Bulagi Dalam Angka"},
    "KCA61": {"name": "Kecamatan Bulagi Selatan Dalam Angka"},
    "KCA62": {"name": "Kecamatan Bulagi Utara Dalam Angka"},
    "KCA70": {"name": "Kecamatan Buko Dalam Angka"},
    "KCA71": {"name": "Kecamatan Buko Selatan Dalam Angka"},
}


def get_publication_menu():
    return (
        "📚 *Publikasi BPS Kabupaten Banggai Kepulauan*\n\n"
        "Ketikkan kode publikasi yang ingin Anda akses.\n\n"
        "DDA. Kabupaten Banggai Kepulauan Dalam Angka\n"
        "PDRBL. Produk Domestik Regional Bruto Kabupaten Banggai Kepulauan Menurut Lapangan Usaha\n"
        "PDRBP. Produk Domestik Regional Bruto Kabupaten Banggai Kepulauan Menurut Pengeluaran\n"
        "Statkesra. Statistik Kesejahteraan Rakyat\n"
        "SKD. Analisis Hasil Survei Kebutuhan Data BPS Kabupaten Banggai Kepulauan\n"
        "KCA30. Kecamatan Totikum Dalam Angka\n"
        "KCA31. Kecamatan Totikum Selatan Dalam Angka\n"
        "KCA40. Kecamatan Tinangkung Dalam Angka\n"
        "KCA41. Kecamatan Tinangkung Selatan Dalam Angka\n"
        "KCA42. Kecamatan Tinangkung Utara Dalam Angka\n"
        "KCA50. Kecamatan Liang Dalam Angka\n"
        "KCA51. Kecamatan Peling Tengah Dalam Angka\n"
        "KCA60. Kecamatan Bulagi Dalam Angka\n"
        "KCA61. Kecamatan Bulagi Selatan Dalam Angka\n"
        "KCA62. Kecamatan Bulagi Utara Dalam Angka\n"
        "KCA70. Kecamatan Buko Dalam Angka\n"
        "KCA71. Kecamatan Buko Selatan Dalam Angka\n\n"
        "Ketik *Pub* untuk tetap di menu Publikasi.\n"
        "Ketik *Menu* untuk kembali ke menu awal.\n"
        "Ketik *Selesai* untuk mengakhiri percakapan."
    )


def get_publication_detail(code: str):
    code = code.strip().upper()
    publication = PUBLICATIONS.get(code)

    if not publication:
        return None

    if code == "DDA":
        return (
            "📖 *Kabupaten Banggai Kepulauan Dalam Angka*\n\n"
            "Tahun 2023\n"
            "s.bps.go.id/dda7201_2023\n\n"
            "Tahun 2022\n"
            "s.bps.go.id/dda7201_2022\n\n"
            "Untuk publikasi selengkapnya dapat mengunjungi:\n"
            "https://bangkepkab.bps.go.id/publication.html\n\n"
            "Ketik *Pub* untuk kembali ke menu Publikasi BPS Kabupaten Banggai Kepulauan\n"
            "Ketik *Menu* untuk kembali ke menu awal.\n"
            "Ketik *Selesai* untuk mengakhiri percakapan."
        )

    return (
        f"📖 *{publication['name']}*\n\n"
        "Untuk mengakses publikasi ini dan edisi lainnya, silakan kunjungi:\n"
        "https://bangkepkab.bps.go.id/publication.html\n\n"
        "Ketik *Pub* untuk kembali ke menu Publikasi BPS Kabupaten Banggai Kepulauan\n"
        "Ketik *Menu* untuk kembali ke menu awal.\n"
        "Ketik *Selesai* untuk mengakhiri percakapan."
    )


def handle_publication(user: UserDB, message: str):
    """Handle publication menu. Caller should manage the user's state."""
    message = message.strip()

    if message.lower() == "pub":
        return get_publication_menu()

    detail = get_publication_detail(message)
    if detail:
        return detail

    return (
        "Kode publikasi tidak ditemukan.\n\n"
        + get_publication_menu()
    )
