import requests

NODE_URL = "http://127.0.0.1:3000"


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

    return response.json()