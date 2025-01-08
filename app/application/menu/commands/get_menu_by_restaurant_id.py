from dataclasses import dataclass
from uuid import UUID

from didiator import Query, QueryHandler

from app.application import dto
from app.application.menu.interface.repository import MenuRepository


@dataclass(frozen=True)
class GetMenuByRestaurantId(Query[dto.Menu]):
    restaurant_id: UUID


class GetMenuByRestaurantIddHandler(QueryHandler[GetMenuByRestaurantId, dto.Menu]):
    def __init__(self, repo: MenuRepository) -> None:
        self._repo = repo

    async def __call__(self, query: GetMenuByRestaurantId) -> dto.Menu:
        menu = await self._repo.get_menu_by_restaurant_id(query.restaurant_id)
        return menu
