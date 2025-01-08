from didiator import (
    Mediator,
    CommandDispatcherImpl,
    QueryDispatcherImpl,
    EventObserverImpl,
    MediatorImpl,
)
from didiator.interface.utils.di_builder import DiBuilder
from didiator.middlewares.di import DiScopes, DiMiddleware
from didiator.middlewares.logging import LoggingMiddleware

from app.application.dish.commands.create_dish import CreateDish, CreateDishHandler
from app.application.dish.commands.get_dish_by_id import GetDishById, GetDishByIdHandler
from app.application.dish.commands.get_dishes import GetDishes, GetDishesHandler
from app.application.dish.commands.get_dish_by_menu_id import (
    GetDishByMenuId,
    GetDishByMenuIddHandler,
)
from app.application.menu.commands.create_menu import CreateMenu, CreateMenuHandler
from app.application.menu.commands.get_menu_by_id import GetMenuById, GetMenuByIdHandler
from app.application.menu.commands.get_menu_by_restaurant_id import (
    GetMenuByRestaurantId,
    GetMenuByRestaurantIddHandler,
)
from app.application.menu.commands.get_menus import GetMenus, GetMenusHandler
from app.application.restaurant.commands.create_restaurant import (
    CreateRestaurant,
    CreateRestaurantHandler,
)
from app.application.restaurant.commands.delete_restaurant import (
    DeleteRestaurant,
    DeleteRestaurantHandler,
)
from app.application.restaurant.commands.get_restaurant_by_id import (
    GetRestaurantById,
    GetRestaurantByIdHandler,
)
from app.application.restaurant.commands.get_restaurant_by_name import (
    GetRestaurantByName,
    GetRestaurantByNameHandler,
)
from app.application.restaurant.commands.get_restaurants import (
    GetRestaurants,
    GetRestaurantsHandler,
)
from app.application.restaurant.commands.update_restaurant import (
    SetRestaurantName,
    SetRestaurantNameHandler,
)


def init_mediator(di_builder: DiBuilder) -> Mediator:
    middlewares = (
        LoggingMiddleware("mediator"),
        DiMiddleware(di_builder, scopes=DiScopes("request")),
    )
    command_dispatcher = CommandDispatcherImpl(middlewares=middlewares)
    query_dispatcher = QueryDispatcherImpl(middlewares=middlewares)
    event_observer = EventObserverImpl(middlewares=middlewares)

    mediator = MediatorImpl(command_dispatcher, query_dispatcher, event_observer)
    return mediator


def setup_mediator(mediator: Mediator) -> None:
    mediator.register_query_handler(GetRestaurants, GetRestaurantsHandler)
    mediator.register_query_handler(GetRestaurantById, GetRestaurantByIdHandler)
    mediator.register_query_handler(GetRestaurantByName, GetRestaurantByNameHandler)
    mediator.register_command_handler(CreateRestaurant, CreateRestaurantHandler)
    mediator.register_command_handler(DeleteRestaurant, DeleteRestaurantHandler)
    mediator.register_command_handler(SetRestaurantName, SetRestaurantNameHandler)
    mediator.register_query_handler(GetMenus, GetMenusHandler)
    mediator.register_query_handler(GetMenuById, GetMenuByIdHandler)
    mediator.register_query_handler(
        GetMenuByRestaurantId, GetMenuByRestaurantIddHandler
    )
    mediator.register_command_handler(CreateMenu, CreateMenuHandler)
    mediator.register_query_handler(GetDishes, GetDishesHandler)
    mediator.register_query_handler(GetDishByMenuId, GetDishByMenuIddHandler)
    mediator.register_query_handler(GetDishById, GetDishByIdHandler)
    mediator.register_command_handler(CreateDish, CreateDishHandler)
