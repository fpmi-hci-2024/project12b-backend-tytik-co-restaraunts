from dataclasses import dataclass
from uuid import UUID

from didiator import Query, QueryHandler

from app.application import dto
from app.application.dish.interface.repository import DishRepository


@dataclass(frozen=True)
class GetDishById(Query[dto.Dish]):
    dish_id: UUID


class GetDishByIdHandler(QueryHandler[GetDishById, dto.Dish]):
    def __init__(self, repo: DishRepository) -> None:
        self._repo = repo

    async def __call__(self, query: GetDishById) -> dto.Dish:
        dish = await self._repo.get_dish_by_id(query.dish_id)
        return dish
