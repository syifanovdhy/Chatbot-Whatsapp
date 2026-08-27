from sqlalchemy.orm import Session

from constants.states import DATA_MENU
from models import UserDB


DATA_CATEGORIES = {
    "D1": "Kependudukan",
    "D2": "Kemiskinan",
    "D3": "PDRB",
    "D4": "Indeks Pembangunan Manusia (IPM)",
    "D5": "Ketenagakerjaan",
    "D6": "Geografis",
}
D1_DATA = {
    "2025": {
            "jumlah_penduduk": " 131.682",
            "kepadatan": "52,91",
            "laju_pertumbuhan": "0,32",
            "rasio_jenis_kelamin": "103",
        },
    "2024": {
        "jumlah_penduduk": "130.008",
        "kepadatan": "52,24",
        "laju_pertumbuhan": "0,32",
        "rasio_jenis_kelamin": "103,03",
    },
    "2023": {
        "jumlah_penduduk": "123.420",
        "kepadatan": "49,59",
        "laju_pertumbuhan": "0,98",
        "rasio_jenis_kelamin": "102,46",
    },
    "2022": {
        "jumlah_penduduk": "121.684",
        "kepadatan": "48,89",
        "laju_pertumbuhan": "0,96",
        "rasio_jenis_kelamin": "103",
    },
}

def get_d1_detail():
    response = """
📊 *Data Kependudukan Kabupaten Banggai Kepulauan*

"""

    for year, data in D1_DATA.items():
        response += f"""Tahun {year}
Jumlah Penduduk: {data['jumlah_penduduk']} jiwa
Kepadatan Penduduk: {data['kepadatan']} jiwa/km²
Laju Pertumbuhan Penduduk: {data['laju_pertumbuhan']}%
Rasio Jenis Kelamin: {data['rasio_jenis_kelamin']}

"""

    response += """Sumber:
BPS Kabupaten Banggai Kepulauan

Ketik *Data* untuk kembali ke menu Data Strategis Kabupaten Banggai Kepulauan.
Ketik *Menu* untuk kembali ke menu awal.
Ketik *Selesai* untuk mengakhiri percakapan.
"""

    return response

D2_DATA = {
    "2025": {
        "garis_kemiskinan": "471.281",
        "penduduk_miskin": "13,92",
        "persentase": "11,49",
    },
    "2024": {
        "garis_kemiskinan": "453.552",
        "penduduk_miskin": "14,86",
        "persentase": "12,32",
    },
    "2023": {
        "garis_kemiskinan": "432.673",
        "penduduk_miskin": "15,50",
        "persentase": "12,90",
    },
    "2022": {
        "garis_kemiskinan": "396.904",
        "penduduk_miskin": "16,07",
        "persentase": "13,44",
    },
}

def get_d2_detail():
    response = """
📊 *Data Kemiskinan Kabupaten Banggai Kepulauan*

"""

    for year, data in D2_DATA.items():
        response += f"""Tahun {year}
Jumlah Penduduk Miskin: {data['penduduk_miskin']} ribu orang
Persentase Penduduk Miskin: {data['persentase']}%
Garis Kemiskinan: Rp{data['garis_kemiskinan']}/kapita/bulan

"""

    response += """Sumber:
BPS Kabupaten Banggai Kepulauan
Susenas Maret

Ketik *Data* untuk kembali ke menu Data Strategis Kabupaten Banggai Kepulauan.
Ketik *Menu* untuk kembali ke menu awal.
Ketik *Selesai* untuk mengakhiri percakapan.
"""

    return response

D3_DATA = {
    "2025": {
        "status": "**",
        "pdrb_adhb": "5.887,34",
        "pdrb_adhk": "3.236,51",
        "pertumbuhan": "4,23",
    },
    "2024": {
        "status": "*",
        "pdrb_adhb": "5.377,32",
        "pdrb_adhk": "3.105,15",
        "pdrb_per_kapita": "43,16",
        "pertumbuhan": "4,03",
    },
    "2023": {
        "status": "",
        "pdrb_adhb": "4.929,03",
        "pdrb_adhk": "2.984,81",
        "pdrb_per_kapita": "39,94",
        "pertumbuhan": "3,99",
    },
    "2022": {
        "status": "",
        "pdrb_adhb": "4.568,79",
        "pdrb_adhk": "2.870,36",
        "pdrb_per_kapita": "37,38",
        "pertumbuhan": "4,94",
    },
    "2021": {
        "status": "",
        "pdrb_adhb": "4.130,12",
        "pdrb_adhk": "2.735,24",
        "pdrb_per_kapita": "34,12",
        "pertumbuhan": "5,07",
    },
}

def get_d3_detail():
    response = """
📊 *Data Perekonomian Kabupaten Banggai Kepulauan*

"""

    for year, data in D3_DATA.items():

        response += f"Tahun {year}{data['status']}\n"

        response += (
            f"PDRB Harga Berlaku (Miliar Rupiah): "
            f"{data['pdrb_adhb']}\n"
        )

        response += (
            f"PDRB Harga Konstan (Miliar Rupiah): "
            f"{data['pdrb_adhk']}\n"
        )

        response += (
            f"Pertumbuhan Ekonomi (%): "
            f"{data['pertumbuhan']}\n\n"
        )

    response += """
*Catatan:
2024: Angka sementara
2025: Angka sangat sementara

Sumber:
BPS Kabupaten Banggai Kepulauan

Untuk data PDRB yang lebih lengkap:
https://tinyurl.com/bps-bangkep-pdrbl-2021-2025

Ketik *Data* untuk kembali ke menu Data Strategis Kabupaten Banggai Kepulauan.
Ketik *Menu* untuk kembali ke menu awal.
Ketik *Selesai* untuk mengakhiri percakapan.
"""

    return response

D4_DATA = {
    "2025": {
        "ipm": "68,44",
    },
    "2024": {
        "ipm": "67,65",
    },
    "2023": {
        "ipm": "67,05",
    },
    "2022": {
        "ipm": "66,30",
    },
    "2021": {
        "ipm": "65,82",
    },
}

def get_d4_detail():
    response = """
📊 *Indeks Pembangunan Manusia Kabupaten Banggai Kepulauan*

"""

    for year, data in D4_DATA.items():
        response += f"""Tahun {year}
IPM: {data['ipm']}

"""

    response += """Sumber:
BPS Kabupaten Banggai Kepulauan

Ketik *Data* untuk kembali ke menu Data Strategis Kabupaten Banggai Kepulauan.
Ketik *Menu* untuk kembali ke menu awal.
Ketik *Selesai* untuk mengakhiri percakapan.
"""

    return response

D5_DATA = {
    "2025": {
        "tpak": "73,35",
        "tpt": "1,67",
    },
    "2024": {
        "tpak": "73,48",
        "tpt": "1,55",
    },
    "2023": {
        "tpak": "72,76",
        "tpt": "1,56",
    },
    "2022": {
        "tpak": "74,63",
        "tpt": "1,48",
    },
    "2021": {
        "tpak": "71,98",
        "tpt": "2,95",
    },
    
}

def get_d5_detail():
    response = """
📊 *Data Ketenagakerjaan Kabupaten Banggai Kepulauan*

"""

    for year, data in D5_DATA.items():
        response += f"""Tahun {year}
Tingkat Partisipasi Angkatan Kerja (TPAK): {data['tpak']}%
Tingkat Pengangguran Terbuka (TPT): {data['tpt']}%

"""

    response += """Sumber:
BPS Kabupaten Banggai Kepulauan

Ketik *Data* untuk kembali ke menu Data Strategis Kabupaten Banggai Kepulauan.
Ketik *Menu* untuk kembali ke menu awal.
Ketik *Selesai* untuk mengakhiri percakapan.
"""

    return response

D6_DATA = {
    "luas_wilayah": "2.488,79 km²",
    "jumlah_kecamatan": "12",
    "jumlah_desa_kelurahan": "144",
}

def get_d6_detail():
    response = """
📊 *Data Geografis Kabupaten Banggai Kepulauan*

Luas Wilayah: {luas} 
Jumlah Kecamatan: {kecamatan}
Jumlah Desa/Kelurahan: {desa}

Sumber:
BPS Kabupaten Banggai Kepulauan

Ketik *Data* untuk kembali ke menu Data Strategis Kabupaten Banggai Kepulauan.
Ketik *Menu* untuk kembali ke menu awal.
Ketik *Selesai* untuk mengakhiri percakapan.
""".format(
        luas=D6_DATA["luas_wilayah"],
        kecamatan=D6_DATA["jumlah_kecamatan"],
        desa=D6_DATA["jumlah_desa_kelurahan"],
    )

    return response

def get_data_menu():
    return """
📊 *Data Strategis Kabupaten Banggai Kepulauan*

Ketikkan Kode Data Strategis Kabupaten Banggai Kepulauan yang ingin anda ketahui.

D1. Kependudukan
D2. Kemiskinan
D3. PDRB
D4. Indeks Pembangunan Manusia (IPM)
D5. Ketenagakerjaan
D6. Geografis
Rincian. Untuk melihat rincian data apa saja yang tersedia di semua kategori di atas

Contoh: Balas dengan *D1* untuk mengetahui data kependudukan.

Ketik *Data* untuk kembali ke menu Data Strategis Kabupaten Banggai Kepulauan
Ketik *Menu* untuk kembali ke menu awal.
Ketik *Selesai* untuk mengakhiri percakapan.
"""


def get_data_detail(code: str):

    code = code.strip().upper()

    if code not in DATA_CATEGORIES:
        return None

    if code == "D1":
        return get_d1_detail()

    if code == "D2":
        return get_d2_detail()

    if code == "D3":
        return get_d3_detail()

    if code == "D4":
        return get_d4_detail()

    if code == "D5":
        return get_d5_detail()

    if code == "D6":
        return get_d6_detail()

    return f"""
📊 *Data {DATA_CATEGORIES[code]}*

Data untuk kategori {DATA_CATEGORIES[code]} sedang dalam proses pengisian.

Ketik *Data* untuk kembali ke menu Data Strategis.
Ketik *Menu* untuk kembali ke menu awal.
Ketik *Selesai* untuk mengakhiri percakapan.
"""


def get_data_rincian():
    return """
📊 *Rincian Data Strategis Kabupaten Banggai Kepulauan*

D1. Kependudukan
- Jumlah Penduduk
- Laju Pertumbuhan Penduduk
- Kepadatan Penduduk

D2. Kemiskinan
- Persentase Penduduk Miskin
- Jumlah Penduduk Miskin
- Garis Kemiskinan

D3. PDRB
- PDRB Harga Berlaku
- PDRB Harga Konstan
- PDRB Per Kapita
- Pertumbuhan Ekonomi

D4. Indeks Pembangunan Manusia (IPM)
- IPM
- Umur Harapan Hidup
- Harapan Lama Sekolah
- Rata-rata Lama Sekolah
- Pengeluaran per Kapita

D5. Ketenagakerjaan
- Tingkat Pengangguran Terbuka
- Tingkat Partisipasi Angkatan Kerja
- Penduduk Bekerja

D6. Geografis
- Luas Wilayah
- Jumlah Kecamatan
- Jumlah Desa/Kelurahan

Ketik kode D1-D6 untuk melihat data.

Ketik *Data* untuk kembali ke menu Data Strategis.
Ketik *Menu* untuk kembali ke menu awal.
Ketik *Selesai* untuk mengakhiri percakapan.
"""


def handle_data(
    db: Session,
    user: UserDB,
    message: str
):
    if user.registration_step != DATA_MENU:
        return None

    message = message.strip()

    # ==========================================
    # KEMBALI KE MENU DATA
    # ==========================================
    if message.lower() == "data":
        return get_data_menu()

    # ==========================================
    # RINCIAN DATA
    # ==========================================
    if message.lower() == "rincian":
        return get_data_rincian()

    # ==========================================
    # DETAIL DATA
    # ==========================================
    detail = get_data_detail(message)

    if detail:
        return detail

    # ==========================================
    # KODE TIDAK DITEMUKAN
    # ==========================================
    return f"""
❌ Kode data *{message}* tidak ditemukan.

Silakan pilih D1-D6 atau ketik *Rincian*.

Ketik *Data* untuk kembali ke menu Data Strategis.
Ketik *Menu* untuk kembali ke menu awal.
"""