from models import UserDB
from services.menu_service import process_menu_choice


def handle_main_menu(
    user: UserDB,
    message: str
):

    if user.registration_step != "MAIN_MENU":
        return None

    return process_menu_choice(message)