from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from didiator import QueryMediator, Mediator, CommandMediator
from starlette import status

from app.application import dto
from app.application.dto import Menu
from app.application.menu.commands.create_menu import CreateMenu
from app.application.menu.commands.get_menu_by_id import GetMenuById
from app.application.menu.commands.get_menu_by_restaurant_id import (
    GetMenuByRestaurantId,
)
from app.application.menu.commands.get_menus import GetMenus
from app.application.menu.interface.reader import GetMenusFilters
from app.domain.common.constant import SortOrder, Empty
from app.domain.common.pagination import Pagination
from app.presentation.providers.stub import Stub
from app.presentation.response.base import OkResponse, ErrorResponse

menu_router = APIRouter(
    prefix="/menus",
    tags=["menus"],
)


@menu_router.get("")
async def get_menus(
    mediator: Annotated[QueryMediator, Depends(Stub(QueryMediator))],
    deleted: bool | None = None,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=1000)] = 1000,
    order: SortOrder = SortOrder.ASC,
):
    menus = await mediator.query(
        GetMenus(
            filters=GetMenusFilters(deleted if deleted is not None else Empty.UNSET),
            pagination=Pagination(
                offset=offset,
                limit=limit,
                order=order,
            ),
        )
    )
    return OkResponse(result=menus)


@menu_router.get(
    "/get_menu_by_restaurant_id/",
    responses={
        status.HTTP_200_OK: {"model": Menu},
        status.HTTP_404_NOT_FOUND: {},
    },
)
async def get_menu_by_restaurant_id(
    mediator: Annotated[QueryMediator, Depends(Stub(QueryMediator))],
    restaurant_id: UUID,
):
    menu = await mediator.query(GetMenuByRestaurantId(restaurant_id=restaurant_id))
    return OkResponse(result=menu)


@menu_router.get(
    "/get_menu_by_id/",
    responses={
        status.HTTP_200_OK: {"model": Menu},
        status.HTTP_404_NOT_FOUND: {},
    },
)
async def get_menu_by_restaurant_id(
    mediator: Annotated[QueryMediator, Depends(Stub(QueryMediator))],
    menu_id: UUID,
):
    menu = await mediator.query(GetMenuById(menu_id=menu_id))
    return OkResponse(result=menu)


@menu_router.post(
    "",
    responses={
        status.HTTP_201_CREATED: {"model": dto.Menu},
    },
)
async def create_menu(
    create_menu_command: CreateMenu,
    mediator: Annotated[Mediator, Depends(Stub(CommandMediator))],
) -> OkResponse[Menu]:
    menu_id = await mediator.send(create_menu_command)
    menu = await mediator.query(GetMenuById(menu_id=menu_id))
    return OkResponse(result=menu)


@menu_router.delete("/delete_menu/")
async def delete_menu(): ...


@menu_router.put("/update_menu/")
async def update_menu(): ...
