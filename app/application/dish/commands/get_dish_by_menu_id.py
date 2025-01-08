from dataclasses import dataclass
from uuid import UUID

from didiator import Query, QueryHandler

from app.application import dto
from app.application.dish.interface.repository import DishRepository


@dataclass(frozen=True)
class GetDishByMenuId(Query[dto.Dish]):
    menu_id: UUID


class GetDishByMenuIddHandler(QueryHandler[GetDishByMenuId, dto.Dish]):
    def __init__(self, repo: DishRepository) -> None:
        self._repo = repo

    async def __call__(self, query: GetDishByMenuId) -> dto.Dish:
        dish = await self._repo.get_dish_by_menu_id(query.menu_id)
        return dish
