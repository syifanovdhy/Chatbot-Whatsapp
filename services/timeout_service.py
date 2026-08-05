import threading
import time

from database import SessionLocal
from models import ConsultationDB
from services.whatsapp_gateway import send_whatsapp_message


TIMEOUT_SECONDS = 10


def start_timeout(consultation_id: int):

    thread = threading.Thread(

        target=timeout_worker,

        args=(consultation_id,),

        daemon=True

    )

    thread.start()


def timeout_worker(consultation_id: int):

    time.sleep(TIMEOUT_SECONDS)

    db = SessionLocal()

    try:

        consultation = db.get(
            ConsultationDB,
            consultation_id
        )

        if consultation is None:
            return

        if consultation.agent_replied:
            return

        if consultation.timeout_sent:
            return

        consultation.timeout_sent = True

        db.commit()

        wa = consultation.user.whatsapp_accounts[0]

        send_whatsapp_message(

            wa.wa_id,

            (
                "🙏 Mohon maaf.\n\n"
                "Saat ini seluruh petugas PST sedang "
                "melayani pengguna lain.\n\n"
                "Mohon tunggu beberapa saat."
            )

        )

    finally:

        db.close()