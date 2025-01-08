from typing import Annotated
from uuid import UUID

from didiator import QueryMediator, Mediator, CommandMediator
from fastapi import APIRouter, Depends, Query
from starlette import status

from app.application import dto
from app.application.dto.restaurant import RestaurantDTO, Restaurant, DeletedRestaurant
from app.application.restaurant.commands.create_restaurant import CreateRestaurant
from app.application.restaurant.commands.delete_restaurant import DeleteRestaurant
from app.application.restaurant.commands.get_restaurant_by_id import GetRestaurantById
from app.application.restaurant.commands.get_restaurant_by_name import (
    GetRestaurantByName,
)
from app.application.restaurant.commands.get_restaurants import GetRestaurants
from app.application.restaurant.commands.update_restaurant import (
    SetRestaurantName,
    SetCuisineName,
)
from app.application.restaurant.exception import (
    RestaurantIdAlreadyExistsError,
    RestaurantIdNotExistError,
    RestaurantNameNotExistError,
)
from app.application.restaurant.interface.reader import GetRestaurantsFilters
from app.domain.common.constant import SortOrder, Empty
from app.domain.common.pagination import Pagination
from app.domain.exceptions.restaurant import (
    RestaurantAlreadyExistsError,
    RestaurantIsDeletedError,
)
from app.presentation.providers.stub import Stub
from app.presentation.response.base import OkResponse, ErrorResponse

restaurant_router = APIRouter(
    prefix="/restaurants",
    tags=["restaurants"],
)


@restaurant_router.get(
    "",
)
async def get_restaurants(
    mediator: Annotated[QueryMediator, Depends(Stub(QueryMediator))],
    deleted: bool | None = None,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=1000)] = 1000,
    order: SortOrder = SortOrder.ASC,
):
    restaurants = await mediator.query(
        GetRestaurants(
            filters=GetRestaurantsFilters(
                deleted if deleted is not None else Empty.UNSET
            ),
            pagination=Pagination(
                offset=offset,
                limit=limit,
                order=order,
            ),
        ),
    )
    return OkResponse(result=restaurants)


@restaurant_router.post(
    "",
    responses={
        status.HTTP_201_CREATED: {"model": dto.Restaurant},
        status.HTTP_409_CONFLICT: {
            "model": ErrorResponse[
                RestaurantAlreadyExistsError | RestaurantIdAlreadyExistsError
            ],
        },
    },
    status_code=status.HTTP_201_CREATED,
)
async def create_restaurant(
    create_restaurant_command: CreateRestaurant,
    mediator: Annotated[Mediator, Depends(Stub(Mediator))],
) -> OkResponse[Restaurant]:
    restaurant_id = await mediator.send(create_restaurant_command)
    restaurant = await mediator.query(GetRestaurantById(restaurant_id=restaurant_id))
    return OkResponse(result=restaurant)


@restaurant_router.get(
    "/restaurant_id/{restaurant_id}",
    responses={
        status.HTTP_200_OK: {"model": Restaurant | DeletedRestaurant},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse[RestaurantIdNotExistError]},
    },
)
async def get_restaurant_by_id(
    restaurant_id: UUID,
    mediator: Annotated[QueryMediator, Depends(Stub(QueryMediator))],
) -> OkResponse[Restaurant]:
    restaurant = await mediator.query(GetRestaurantById(restaurant_id=restaurant_id))
    return OkResponse(result=restaurant)


@restaurant_router.get(
    "/restaurant_name/{name}",
    responses={
        status.HTTP_200_OK: {"model": Restaurant},
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse[RestaurantNameNotExistError]
        },
    },
)
async def get_restaurant_by_name(
    name: str,
    mediator: Annotated[QueryMediator, Depends(Stub(QueryMediator))],
) -> OkResponse[Restaurant]:
    restaurant = await mediator.query(GetRestaurantByName(name=name))
    return OkResponse(result=restaurant)


@restaurant_router.delete(
    "/delete_restaurant/{restaraunt_id}",
    responses={
        status.HTTP_200_OK: {"model": DeletedRestaurant},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse[RestaurantIdNotExistError]},
        status.HTTP_409_CONFLICT: {"model": ErrorResponse[RestaurantIsDeletedError]},
    },
)
async def delete_restaurant(
    restaurant_id: UUID,
    mediator: Annotated[CommandMediator, Depends(Stub(CommandMediator))],
) -> OkResponse[None]:
    restaurant = await mediator.send(DeleteRestaurant(restaurant_id=restaurant_id))
    return OkResponse(result=restaurant)


@restaurant_router.put(
    "/name",
    responses={
        status.HTTP_200_OK: {"model": dto.Restaurant},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse[RestaurantIdNotExistError]},
        status.HTTP_409_CONFLICT: {
            "model": ErrorResponse[
                RestaurantAlreadyExistsError | RestaurantIsDeletedError
            ],
        },
    },
)
async def set_restaurant_name(
    restaurant_id: UUID,
    name: str,
    mediator: Annotated[CommandMediator, Depends(Stub(CommandMediator))],
) -> OkResponse[None]:
    restaurant = await mediator.send(
        SetRestaurantName(restaurant_id=restaurant_id, name=name)
    )
    return OkResponse(result=restaurant)


@restaurant_router.put(
    "/cuisine_name",
    responses={
        status.HTTP_200_OK: {"model": dto.Restaurant},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse[RestaurantIdNotExistError]},
        status.HTTP_409_CONFLICT: {
            "model": ErrorResponse[
                RestaurantAlreadyExistsError | RestaurantIsDeletedError
            ],
        },
    },
)
async def set_cuisine_name(
    restaurant_id: UUID,
    cuisine_name: str,
    mediator: Annotated[CommandMediator, Depends(Stub(CommandMediator))],
) -> OkResponse[None]:
    restaurant = await mediator.send(
        SetCuisineName(restaurant_id=restaurant_id, cuisine_name=cuisine_name)
    )
    return OkResponse(result=restaurant)
