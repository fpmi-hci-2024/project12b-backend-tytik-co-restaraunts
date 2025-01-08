from app.domain import entity
from app.domain.entity.restaurant import (
    RestaurantId,
    RestaurantName,
    RestaurantCuisineName,
    RestaurantLogoUrl,
)
from app.infrastructure.db.models import Restaurant


def convert_db_event_model_to_entity(restaurant: Restaurant) -> entity.Restaurant:
    return entity.Restaurant(
        id=RestaurantId(restaurant.id),
        name=RestaurantName(restaurant.name),
        cuisine_name=RestaurantCuisineName(restaurant.cuisine_name),
        logo_url=RestaurantLogoUrl(restaurant.logo_url),
        is_deleted=restaurant.is_deleted,
    )
