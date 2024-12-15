from app.domain import entity
from app.infrastructure.db.models import Restaurant


def convert_restaurant_dto_to_db_model(restaurant: entity.Restaurant) -> Restaurant:
    return Restaurant(
        id=restaurant.id.value,
        name=restaurant.name.value,
        cuisine_name=restaurant.cuisine_name.value,
        is_deleted=restaurant.is_deleted.value,
    )
