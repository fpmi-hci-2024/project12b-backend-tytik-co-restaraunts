import logging
from functools import partial
from typing import Callable, Awaitable

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette import status
from starlette.requests import Request

from app.application.restaurant.exception import (
    RestaurantIdNotExistError,
    RestaurantNameAlreadyExistsError,
    RestaurantIdAlreadyExistsError,
    RestaurantNameNotExistError,
)
from app.domain.common.exception import AppError
from app.domain.exceptions.restaurant import RestaurantIsDeletedError
from app.presentation.response.base import ErrorData, ErrorResponse

logger = logging.getLogger(__name__)


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, error_handler(500))
    app.add_exception_handler(
        RestaurantIdNotExistError, error_handler(status.HTTP_404_NOT_FOUND)
    )
    app.add_exception_handler(
        RestaurantNameNotExistError, error_handler(status.HTTP_404_NOT_FOUND)
    )
    app.add_exception_handler(
        RestaurantIdAlreadyExistsError, error_handler(status.HTTP_409_CONFLICT)
    )
    app.add_exception_handler(
        RestaurantNameAlreadyExistsError, error_handler(status.HTTP_409_CONFLICT)
    )
    app.add_exception_handler(
        RestaurantIsDeletedError, error_handler(status.HTTP_409_CONFLICT)
    )
    app.add_exception_handler(Exception, unknown_exception_handler)


def error_handler(status_code: int) -> Callable[..., Awaitable[ORJSONResponse]]:
    return partial(app_error_handler, status_code=status_code)


async def app_error_handler(
    request: Request, err: AppError, status_code: int
) -> ORJSONResponse:
    return await handle_error(
        request=request,
        err=err,
        err_data=ErrorData(title=err.title, data=err),
        status=err.status,
        status_code=status_code,
    )


async def unknown_exception_handler(request: Request, err: Exception) -> ORJSONResponse:
    logger.error("Handle error", exc_info=err, extra={"error": err})
    logger.exception("Unknown error occurred", exc_info=err, extra={"error": err})
    return ORJSONResponse(
        ErrorResponse(error=ErrorData(data=err)),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


async def handle_error(
    request: Request,
    err: Exception,
    err_data: ErrorData,
    status: int,
    status_code: int,
) -> ORJSONResponse:
    logger.error("Handle error", exc_info=err, extra={"error": err})
    return ORJSONResponse(
        ErrorResponse(error=err_data, status=status),
        status_code=status_code,
    )
