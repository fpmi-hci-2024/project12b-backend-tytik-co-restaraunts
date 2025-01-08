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
): ...


@dish_router.post("create_dish/{menu_id}")
async def create_dish(menu_id: UUID): ...


@dish_router.put("update_dish/{menu_id}")
async def update_dish(menu_id: UUID): ...
