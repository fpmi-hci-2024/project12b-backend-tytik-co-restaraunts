from app.domain import entity
from app.infrastructure.db.models import Menu


def convert_menu_dto_to_db_model(menu: entity.Menu) -> Menu:
    return Menu(
        id=menu.id.value,
        name=menu.name.value,
        restaurant_id=menu.restaurant_id.value,
        logo_url=menu.logo_url.value,
        is_deleted=menu.is_deleted,
    )
