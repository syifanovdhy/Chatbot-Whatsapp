import re

def parse_registration(message: str):

    nama = None
    instansi = None
    email = None

    lines = message.splitlines()

    for line in lines:

        line = line.strip()

        if line.lower().startswith("nama:"):
            nama = line.split(":", 1)[1].strip()

        elif line.lower().startswith("instansi:"):
            instansi = line.split(":", 1)[1].strip()

        elif line.lower().startswith("email:"):
            email = line.split(":", 1)[1].strip()

    if not nama or not instansi or email is None:
        return None

    return {
        "nama": nama,
        "instansi": instansi,
        "email": email
    }