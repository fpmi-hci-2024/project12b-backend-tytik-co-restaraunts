from uuid import UUID

from fastapi import APIRouter

menu_router = APIRouter(
    prefix="/menus",
    tags=["menus"],
)


@menu_router.get("/get_menu/{restaurant_id}")
async def get_menu_for_cafe(restaurant_id: UUID): ...


@menu_router.post("/create_menu/")
async def create_menu(): ...


@menu_router.put("/update_menu/")
async def update_menu(): ...
