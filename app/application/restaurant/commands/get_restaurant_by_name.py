from dataclasses import dataclass

from didiator import Query, QueryHandler

from app.application.dto import Restaurant
from app.application.restaurant.interface.repository import RestaurantRepository


@dataclass(frozen=True)
class GetRestaurantByName(Query[Restaurant]):
    name: str


class GetRestaurantByNameHandler(QueryHandler[GetRestaurantByName, Restaurant]):
    def __init__(self, repo: RestaurantRepository) -> None:
        self._repo = repo

    async def __call__(self, query: GetRestaurantByName) -> Restaurant:
        restaurant = await self._repo.get_restaurant_by_name(query.name)
        return restaurant
