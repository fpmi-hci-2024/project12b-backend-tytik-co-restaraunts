from di import bind_by_type, Container
from di.api.providers import DependencyProviderType
from di.api.scopes import Scope
from di.dependent import Dependent
from di.executors import AsyncExecutor
from didiator import Mediator, QueryMediator, CommandMediator, EventMediator

from didiator.interface.utils.di_builder import DiBuilder
from didiator.utils.di_builder import DiBuilderImpl
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession

from app.application.dish.interface.repository import DishRepository
from app.application.menu.interface.repository import MenuRepository
from app.application.restaurant.interface.repository import RestaurantRepository
from app.application.uow.common import UnitOfWork
from app.infrastructure.db.main import (
    build_sa_engine,
    build_sa_session_factory,
    build_sa_session,
)
from app.infrastructure.db.repository.dish import DishRepositoryImpl
from app.infrastructure.db.repository.menu import MenuRepositoryImpl
from app.infrastructure.db.repository.restaraunt import RestaurantRepositoryImpl
from app.infrastructure.uow import build_uow


def get_mediator() -> Mediator:
    raise NotImplemented


def init_di_builder() -> DiBuilder:
    di_container = Container()
    di_executor = AsyncExecutor()
    di_scopes = ["app", "request"]
    di_builder = DiBuilderImpl(di_container, di_executor, di_scopes=di_scopes)
    return di_builder


def setup_di_builder(di_builder: DiBuilder) -> None:
    di_builder.bind(
        bind_by_type(Dependent(lambda *args: di_builder, scope="app"), DiBuilder)
    )
    di_builder.bind(bind_by_type(Dependent(build_uow, scope="request"), UnitOfWork))
    setup_mediator_factory(di_builder, get_mediator, "request")
    setup_db_factories(di_builder)


def setup_mediator_factory(
    di_builder: DiBuilder,
    mediator_factory: DependencyProviderType,
    scope: Scope,
) -> None:
    di_builder.bind(bind_by_type(Dependent(mediator_factory, scope=scope), Mediator))
    di_builder.bind(
        bind_by_type(Dependent(mediator_factory, scope=scope), QueryMediator)
    )
    di_builder.bind(
        bind_by_type(Dependent(mediator_factory, scope=scope), CommandMediator)
    )
    di_builder.bind(
        bind_by_type(Dependent(mediator_factory, scope=scope), EventMediator)
    )


def setup_db_factories(di_builder: DiBuilder) -> None:
    di_builder.bind(bind_by_type(Dependent(build_sa_engine, scope="app"), AsyncEngine))
    di_builder.bind(
        bind_by_type(
            Dependent(build_sa_session_factory, scope="app"),
            async_sessionmaker[AsyncSession],
        ),
    )
    di_builder.bind(
        bind_by_type(Dependent(build_sa_session, scope="request"), AsyncSession)
    )
    di_builder.bind(
        bind_by_type(
            Dependent(RestaurantRepositoryImpl, scope="request"),
            RestaurantRepository,
            covariant=True,
        )
    )
    di_builder.bind(
        bind_by_type(
            Dependent(MenuRepositoryImpl, scope="request"),
            MenuRepository,
            covariant=True,
        )
    )
    di_builder.bind(
        bind_by_type(
            Dependent(DishRepositoryImpl, scope="request"),
            DishRepository,
            covariant=True,
        )
    )
