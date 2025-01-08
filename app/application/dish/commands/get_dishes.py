from dataclasses import dataclass

from didiator import Query, QueryHandler

from app.application import dto
from app.application.dish.interface.reader import GetDishesFilters
from app.application.dish.interface.repository import DishRepository
from app.domain.common.pagination import Pagination


@dataclass(frozen=True)
class GetDishes(Query[dto.Dishes]):
    filters: GetDishesFilters
    pagination: Pagination


class GetDishesHandler(QueryHandler[GetDishes, dto.Dishes]):
    def __init__(self, repo: DishRepository) -> None:
        self._repo = repo

    async def __call__(self, query: GetDishes) -> dto.Dishes:
        dishes = await self._repo.get_dishes(query.pagination, query.filters)
        return dishes
