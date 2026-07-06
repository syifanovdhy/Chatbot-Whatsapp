from sqlalchemy.orm import Session


def process_chat(
    db: Session,
    message: str,
    wa_id: str,
    push_name: str
):
    """
    Seluruh logika chatbot akan berada di sini.
    """

    return "Belum diimplementasikan."