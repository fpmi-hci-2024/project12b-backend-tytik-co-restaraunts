from dataclasses import dataclass
from uuid import UUID

from didiator import Query, QueryHandler

from app.application import dto
from app.application.menu.interface.repository import MenuRepository


@dataclass(frozen=True)
class GetMenuById(Query[dto.Menu]):
    menu_id: UUID


class GetMenuByIdHandler(QueryHandler[GetMenuById, dto.Menu]):
    def __init__(self, repo: MenuRepository) -> None:
        self._repo = repo

    async def __call__(self, query: GetMenuById) -> dto.Menu:
        menu = await self._repo.get_menu_by_id(query.menu_id)
        return menu
