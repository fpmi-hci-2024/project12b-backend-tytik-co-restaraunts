from di import ScopeState
from didiator import Mediator, CommandMediator, QueryMediator, EventMediator
from didiator.interface.utils.di_builder import DiBuilder
from fastapi import FastAPI

from app.presentation.providers.di import StateProvider, get_di_builder, get_di_state
from app.presentation.providers.mediator import MediatorProvider
from app.presentation.providers.stub import Stub


def setup_providers(
    app: FastAPI,
    mediator: Mediator,
    di_builder: DiBuilder,
    di_state: ScopeState | None = None,
) -> None:
    mediator_provider = MediatorProvider(mediator)

    app.dependency_overrides[Stub(Mediator)] = mediator_provider.build
    app.dependency_overrides[Stub(CommandMediator)] = mediator_provider.build
    app.dependency_overrides[Stub(QueryMediator)] = mediator_provider.build
    app.dependency_overrides[Stub(EventMediator)] = mediator_provider.build

    state_provider = StateProvider(di_state)

    app.dependency_overrides[get_di_builder] = lambda: di_builder
    app.dependency_overrides[get_di_state] = state_provider.build
