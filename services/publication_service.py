from sqlalchemy.orm import Session

from constants.states import PUBLICATION_MENU
from models import UserDB


PUBLICATIONS = {
    "DDA": {
        "name": "Kabupaten Banggai Kepulauan Dalam Angka",
        "links": {
        "2026": "https://tinyurl.com/bps-bangkep-dda-2026",
        "2025": "https://tinyurl.com/bps-bangkep-dda-2025",
        "2024": "https://tinyurl.com/bps-bangkep-dda-2024"
        }
    },

    "PDRBL": {
        "name": "Produk Domestik Regional Bruto Kabupaten Banggai Kepulauan Menurut Lapangan Usaha",
        "links": {
        "2026": "https://tinyurl.com/bps-bangkep-pdrbl-2021-2025",
        "2025": "https://tinyurl.com/bps-bangkep-pdrbl-2020-2024",
        "2024": "https://tinyurl.com/bps-bangkep-pdrbl-2019-2023"
        }
    },

    "PDRBP": {
        "name": "Produk Domestik Regional Bruto Kabupaten Banggai Kepulauan Menurut Pengeluaran",
        "links": {
        "2026": "https://tinyurl.com/bps-bangkep-pdrbp-2021-2025",
        "2025": "https://tinyurl.com/bps-bangkep-pdrbp-2020-2024"
        }
    },

    "STATKESRA": {
        "name": "Statistik Kesejahteraan Rakyat",
        "links": {
        "2025": "https://tinyurl.com/bps-bangkep-statkesra-2025",
        "2024": "https://tinyurl.com/bps-bangkep-statkesra-2024"
        }
    },

    "SKD": {
        "name": "Analisis Hasil Survei Kebutuhan Data BPS Kabupaten Banggai Kepulauan",
        "links": {
        "2025": "https://tinyurl.com/bps-bangkep-skd-2025",
        "2024": "https://tinyurl.com/bps-bangkep-skd-2024"
        }
    },

    "KCA30": {
        "name": "Kecamatan Totikum Dalam Angka",
        "links": {
        "2025": "https://tinyurl.com/bps-bangkep-kca30-2025"
        }
    },

    "KCA31": {
        "name": "Kecamatan Totikum Selatan Dalam Angka",
        "links": {
        "2025": "https://tinyurl.com/bps-bangkep-kca31-2025"
        }
    },

    "KCA40": {
        "name": "Kecamatan Tinangkung Dalam Angka",
        "links": {
        "2025": "https://tinyurl.com/bps-bangkep-kca40-2025"
        }
    },

    "KCA41": {
        "name": "Kecamatan Tinangkung Selatan Dalam Angka",
        "links": {
        "2025": "https://tinyurl.com/bps-bangkep-kca41-2025"
        }
    },

    "KCA42": {
        "name": "Kecamatan Tinangkung Utara Dalam Angka",
        "links": {
        "2025": "https://tinyurl.com/bps-bangkep-kca42-2025"
        }
    },

    "KCA50": {
        "name": "Kecamatan Liang Dalam Angka",
        "links": {
        "2025": "https://tinyurl.com/bps-bangkep-kca50-2025"
        }
    },

    "KCA51": {
        "name": "Kecamatan Peling Tengah Dalam Angka",
        "links": {
        "2025": "https://tinyurl.com/bps-bangkep-kca51-2025"
        }
    },

    "KCA60": {
        "name": "Kecamatan Bulagi Dalam Angka",
        "links": {
        "2025": "https://tinyurl.com/bps-bangkep-kca60-2025"
        }
    },

    "KCA61": {
        "name": "Kecamatan Bulagi Selatan Dalam Angka",
        "links": {
        "2025": "https://tinyurl.com/bps-bangkep-kca61-2025"
        }
    },

    "KCA62": {
        "name": "Kecamatan Bulagi Utara Dalam Angka",
        "links": {
        "2025": "https://tinyurl.com/bps-bangkep-kca62-2025"
        }
    },

    "KCA70": {
        "name": "Kecamatan Buko Dalam Angka",
        "links": {
        "2025": "https://tinyurl.com/bps-bangkep-kca70-2025"
        }
    },

    "KCA71": {
        "name": "Kecamatan Buko Selatan Dalam Angka",
        "links": {
        "2025": "https://tinyurl.com/bps-bangkep-kca71-2025"
        }
    }
}


def get_publication_menu():
    return """
📚 *Publikasi BPS Kabupaten Banggai Kepulauan*

Ketikkan Kode Publikasi yang ingin anda akses.

*Publikasi Umum:*
1. *DDA* — Kabupaten Banggai Kepulauan Dalam Angka
2. *PDRBL* — Produk Domestik Regional Bruto Kabupaten Banggai Kepulauan Menurut Lapangan Usaha
3. *PDRBP* — Produk Domestik Regional Bruto Kabupaten Banggai Kepulauan Menurut Pengeluaran
4. *Statkesra* — Statistik Kesejahteraan Rakyat
5. *SKD* — Analisis Hasil Survei Kebutuhan Data BPS Kabupaten Banggai Kepulauan

*Publikasi Kecamatan:*
6. *KCA30* — Kecamatan Totikum Dalam Angka
7. *KCA31* — Kecamatan Totikum Selatan Dalam Angka
8. *KCA40* — Kecamatan Tinangkung Dalam Angka
9. *KCA41* — Kecamatan Tinangkung Selatan Dalam Angka
10. *KCA42* — Kecamatan Tinangkung Utara Dalam Angka
11. *KCA50* — Kecamatan Liang Dalam Angka
12. *KCA51* — Kecamatan Peling Tengah Dalam Angka
13. *KCA60* — Kecamatan Bulagi Dalam Angka
14. *KCA61* — Kecamatan Bulagi Selatan Dalam Angka
15. *KCA62* — Kecamatan Bulagi Utara Dalam Angka
16. *KCA70* — Kecamatan Buko Dalam Angka
17. *KCA71* — Kecamatan Buko Selatan Dalam Angka

💡 *Contoh:*
Ketik *DDA* untuk mengakses Kabupaten Banggai Kepulauan Dalam Angka.

Ketik *Pub* untuk menampilkan kembali daftar publikasi.
Ketik *Menu* atau *0* untuk kembali ke menu utama.
Ketik *Selesai* untuk mengakhiri percakapan.
"""


def get_publication_detail(code: str):
    code = code.strip().upper()

    if code not in PUBLICATIONS:
        return None

    publication = PUBLICATIONS[code]

    response = f"""
📖 *{publication['name']}*

"""

    for year, link in publication["links"].items():
        response += f"{year}\n{link}\n\n"

    response += """
Publikasi Lainnya dapat diakses melalui website bPS Kabupaten Banggai Kepulauan 
https://www.bangkepkab.bps.go.id
Ketik *Pub* untuk kembali ke menu Publikasi BPS Kabupaten Banggai Kepulauan
Ketik *Menu* untuk kembali ke menu awal.
Ketik *Selesai* untuk mengakhiri percakapan."""

    return response


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