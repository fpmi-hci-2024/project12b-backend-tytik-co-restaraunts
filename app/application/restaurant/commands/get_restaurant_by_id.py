from dataclasses import dataclass
from uuid import UUID

from didiator import Query, QueryHandler

from app.application import dto
from app.application.restaurant.interface.repository import RestaurantRepository


@dataclass(frozen=True)
class GetRestaurantById(Query[dto.Restaurant]):
    restaurant_id: UUID


class GetRestaurantByIdHandler(QueryHandler[GetRestaurantById, dto.Restaurant]):
    def __init__(self, repo: RestaurantRepository) -> None:
        self._repo = repo

    async def __call__(self, query: GetRestaurantById) -> dto.Restaurant:
        restaurant = await self._repo.get_restaurant_by_id(query.restaurant_id)
        return restaurant
