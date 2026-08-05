from models import UserDB

from constants.states import MAIN_MENU

from services.menu_service import process_menu_choice


def handle_menu(
    user: UserDB,
    message: str
):

    if user.registration_step != MAIN_MENU:
        return None

    return process_menu_choice(message)