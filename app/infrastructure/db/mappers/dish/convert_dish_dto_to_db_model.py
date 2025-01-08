from app.domain import entity
from app.infrastructure.db.models import Dish


def convert_dish_dto_to_db_model(dish: entity.Dish) -> Dish:
    return Dish(
        id=dish.id.value,
        name=dish.name.value,
        price=dish.price.value,
        menu_id=dish.menu_id.value,
        logo_url=dish.logo_url.value,
        dishes_type=dish.dishes_type.value,
        ingredients=dish.ingredients.value,
        is_deleted=dish.is_deleted,
    )
