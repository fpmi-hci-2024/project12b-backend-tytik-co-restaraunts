from uuid import UUID

from didiator import QueryMediator
from fastapi import APIRouter, Query
from fastapi.params import Depends
from sqlalchemy.sql.annotation import Annotated

from app.domain.common.constant import SortOrder
from app.presentation.providers.stub import Stub

dish_router = APIRouter(
    prefix="/dishes",
    tags=["dishes"],
)


@dish_router.get("get_dishes/{menu_id}")
async def get_dishes(
    menu_id: UUID,
    mediator: Annotated[QueryMediator, Depends(Stub(QueryMediator))],
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=1000)] = 1000,
    order: SortOrder = SortOrder.ASC,
): ...


@dish_router.post("create_dish/{menu_id}")
async def create_dish(menu_id: UUID): ...


@dish_router.put("update_dish/{menu_id}")
async def update_dish(menu_id: UUID): ...
