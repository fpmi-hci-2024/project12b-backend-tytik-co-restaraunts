from fastapi import FastAPI

from app.presentation.api.default import default_router
from app.presentation.api.restaurant import restaurant_router
from app.presentation.exception_controllers.exceptions import setup_exception_handlers


def setup_controllers(app: FastAPI) -> None:
    app.include_router(default_router)
    app.include_router(restaurant_router)
    setup_exception_handlers(app)
