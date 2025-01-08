from dataclasses import dataclass

from didiator import QueryHandler, Query

from app.application import dto
from app.application.restaurant.interface.reader import GetRestaurantsFilters
from app.application.restaurant.interface.repository import RestaurantRepository
from app.domain.common.pagination import Pagination


@dataclass(frozen=True)
class GetRestaurants(Query[dto.Restaurants]):
    filters: GetRestaurantsFilters
    pagination: Pagination


class GetRestaurantsHandler(QueryHandler[GetRestaurants, dto.Restaurants]):
    def __init__(self, repo: RestaurantRepository) -> None:
        self._repo = repo

    async def __call__(self, query: GetRestaurants) -> dto.Restaurants:
        restaurants = await self._repo.get_restaurants(query.pagination, query.filters)
        return restaurants
