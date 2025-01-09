from dataclasses import dataclass
from uuid import UUID

from didiator import Query, QueryHandler

from app.application import dto
from app.application.dish.interface.reader import GetDishesFilters
from app.application.dish.interface.repository import DishRepository
from app.domain.common.pagination import Pagination


@dataclass(frozen=True)
class GetDishByMenuId(Query[dto.Dishes]):
    menu_id: UUID
    filters: GetDishesFilters
    pagination: Pagination


class GetDishByMenuIddHandler(QueryHandler[GetDishByMenuId, dto.Dishes]):
    def __init__(self, repo: DishRepository) -> None:
        self._repo = repo

    async def __call__(self, query: GetDishByMenuId) -> dto.Dishes:
        dishes = await self._repo.get_dish_by_menu_id(
            menu_id=query.menu_id, pagination=query.pagination, filters=query.filters
        )
        return dishes
