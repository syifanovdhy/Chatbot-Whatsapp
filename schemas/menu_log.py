from pydantic import BaseModel
from schemas.menu import MenuType

class MenuLogCreate(BaseModel):
    user_id: int
    menu_type: MenuType