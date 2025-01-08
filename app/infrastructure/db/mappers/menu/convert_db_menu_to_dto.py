from app.application import dto
from app.infrastructure.db.models import Menu


def convert_db_event_model_to_dto(menu: Menu) -> dto.Menu:
    return dto.Menu(
        id=menu.id,
        name=menu.name,
        restaurant_id=menu.restaurant_id,
        logo_url=menu.logo_url,
        is_deleted=menu.is_deleted,
    )
