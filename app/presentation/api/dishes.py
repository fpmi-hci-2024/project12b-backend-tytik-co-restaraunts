from typing import Annotated
from uuid import UUID

from didiator import QueryMediator, Mediator, CommandMediator
from fastapi import APIRouter, Depends, Query
from starlette import status

from app.application import dto
from app.application.dish.commands.create_dish import CreateDish
from app.application.dish.commands.get_dish_by_id import GetDishById
from app.application.dish.commands.get_dish_by_menu_id import GetDishByMenuId
from app.application.dish.commands.get_dishes import GetDishes
from app.application.dish.interface.reader import GetDishesFilters
from app.domain.common.constant import SortOrder, Empty
from app.domain.common.pagination import Pagination
from app.domain.entity import Dish
from app.presentation.providers.stub import Stub
from app.presentation.response.base import OkResponse

dish_router = APIRouter(
    prefix="/dishes",
    tags=["dishes"],
)


@dish_router.get("")
async def get_dishes(
    mediator: Annotated[QueryMediator, Depends(Stub(QueryMediator))],
    deleted: bool | None = None,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=1000)] = 1000,
    order: SortOrder = SortOrder.ASC,
):
    dishes = await mediator.query(
        GetDishes(
            filters=GetDishesFilters(deleted if deleted is not None else Empty.UNSET),
            pagination=Pagination(
                offset=offset,
                limit=limit,
                order=order,
            ),
        )
    )
    return OkResponse(result=dishes)


@dish_router.get(
    "/get_dish_by_menu_id/",
)
async def get_dishes_by_menu_id(
    mediator: Annotated[QueryMediator, Depends(Stub(QueryMediator))],
    menu_id: UUID,
    deleted: bool | None = None,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=1000)] = 1000,
    order: SortOrder = SortOrder.ASC,
):
    dishes = await mediator.query(
        GetDishByMenuId(
            menu_id=menu_id,
            filters=GetDishesFilters(deleted if deleted is not None else Empty.UNSET),
            pagination=Pagination(
                offset=offset,
                limit=limit,
                order=order,
            ),
        )
    )
    return OkResponse(result=dishes)


@dish_router.get(
    "/get_dish_by_id/",
    responses={
        status.HTTP_200_OK: {"model": Dish},
        status.HTTP_404_NOT_FOUND: {},
    },
)
async def get_dish_by_id(
    mediator: Annotated[QueryMediator, Depends(Stub(QueryMediator))],
    dish_id: UUID,
):
    dish = await mediator.query(GetDishById(dish_id=dish_id))
    return OkResponse(result=dish)


@dish_router.post(
    "",
    responses={
        status.HTTP_201_CREATED: {"model": dto.Dish},
    },
)
async def create_dish(
    create_dish_command: CreateDish,
    mediator: Annotated[Mediator, Depends(Stub(CommandMediator))],
) -> OkResponse[Dish]:
    dish_id = await mediator.send(create_dish_command)
    menu = await mediator.query(GetDishById(dish_id=dish_id))
    return OkResponse(result=menu)


@dish_router.delete("/delete_dish/")
async def delete_dish(): ...


@dish_router.put("/update_dish/")
async def update_dish(): ...
