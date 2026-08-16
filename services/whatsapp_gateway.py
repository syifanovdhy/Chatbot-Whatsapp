import requests

from config import NODE_URL


def send_whatsapp_message(
    wa_id: str,
    message: str
):

    response = requests.post(
        f"{NODE_URL}/send-message",
        json={
            "wa_id": wa_id,
            "message": message
        },
        timeout=10
    )

    response.raise_for_status()

    return response.json()