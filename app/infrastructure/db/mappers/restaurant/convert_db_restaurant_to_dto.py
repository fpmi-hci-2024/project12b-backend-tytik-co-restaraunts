from app.application import dto
from app.infrastructure.db.models import Restaurant


def convert_db_event_model_to_dto(restaurant: Restaurant) -> dto.Restaurant:
    return dto.Restaurant(
        id=restaurant.id,
        name=restaurant.name,
        cuisine_name=restaurant.cuisine_name,
        is_deleted=restaurant.is_deleted
    )
