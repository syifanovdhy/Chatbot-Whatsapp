import threading
import time
import logging

from database import SessionLocal
from models import ConsultationDB
from services.whatsapp_gateway import send_whatsapp_message


TIMEOUT_SECONDS = 10
MAX_SEND_ATTEMPTS = 3
RETRY_DELAY_SECONDS = 5
logger = logging.getLogger(__name__)


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

        whatsapp_accounts = consultation.user.whatsapp_accounts
        if not whatsapp_accounts:
            logger.error(
                "Notifikasi timeout tidak dapat dikirim: konsultasi %s tidak memiliki akun WhatsApp.",
                consultation_id,
            )
            return

        wa = whatsapp_accounts[0]

        timeout_message = (
            "Mohon maaf.\n\n"
            "Saat ini seluruh petugas PST sedang melayani pengguna lain.\n\n"
            "Mohon tunggu beberapa saat.\n\n"
            "Jika ingin membatalkan permintaan konsultasi, ketik *batal*."
        )

        for attempt in range(1, MAX_SEND_ATTEMPTS + 1):
            try:
                send_whatsapp_message(wa.wa_id, timeout_message)
                break
            except Exception:
                if attempt == MAX_SEND_ATTEMPTS:
                    raise

                logger.warning(
                    "Percobaan %s/%s pengiriman timeout untuk konsultasi %s gagal.",
                    attempt,
                    MAX_SEND_ATTEMPTS,
                    consultation_id,
                    exc_info=True,
                )
                time.sleep(RETRY_DELAY_SECONDS)

        # Tandai hanya setelah WhatsApp bridge mengonfirmasi pengiriman.
        consultation.timeout_sent = True
        db.commit()

    except Exception:
        db.rollback()
        logger.exception(
            "Gagal mengirim notifikasi timeout untuk konsultasi %s.",
            consultation_id,
        )

    finally:

        db.close()
