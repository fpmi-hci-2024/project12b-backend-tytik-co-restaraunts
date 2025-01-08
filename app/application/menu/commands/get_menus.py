from dataclasses import dataclass

from didiator import Query, QueryHandler

from app.application import dto
from app.application.menu.interface.reader import GetMenusFilters
from app.application.menu.interface.repository import MenuRepository
from app.domain.common.pagination import Pagination


@dataclass(frozen=True)
class GetMenus(Query[dto.Menus]):
    filters: GetMenusFilters
    pagination: Pagination


class GetMenusHandler(QueryHandler[GetMenus, dto.Menus]):
    def __init__(self, repo: MenuRepository) -> None:
        self._repo = repo

    async def __call__(self, query: GetMenus) -> dto.Menus:
        menus = await self._repo.get_menus(query.pagination, query.filters)
        return menus
