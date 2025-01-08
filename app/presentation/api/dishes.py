from uuid import UUID

from fastapi import APIRouter

dish_router = APIRouter(
    prefix="/dishes",
    tags=["dishes"],
)


@dish_router.get("get_dishes/{menu_id}")
async def get_dishes(menu_id: UUID): ...


@dish_router.post("create_dish/{menu_id}")
async def create_dish(menu_id: UUID): ...


@dish_router.put("update_dish/{menu_id}")
async def update_dish(menu_id: UUID): ...
