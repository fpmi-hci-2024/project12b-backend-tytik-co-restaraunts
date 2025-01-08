from app.application import dto
from app.infrastructure.db.models import Dish


def convert_db_event_model_to_dto(dish: Dish) -> dto.Dish:
    return dto.Dish(
        id=dish.id,
        name=dish.name,
        price=dish.price,
        menu_id=dish.menu_id,
        logo_url=dish.logo_url,
        dishes_type=dish.dishes_type,
        ingredients=dish.ingredients,
        is_deleted=dish.is_deleted,
    )
