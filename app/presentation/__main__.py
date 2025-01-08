import asyncio

from app.infrastructure.config_loader import load_config
from app.infrastructure.di.main import init_di_builder, setup_di_builder
from app.infrastructure.mediator.main import setup_mediator, init_mediator
from app.presentation.api.main import run_api, init_api
from app.presentation.config import Config, setup_di_builder_config


async def main() -> None:
    config = load_config(Config)

    di_builder = init_di_builder()
    setup_di_builder(di_builder)
    setup_di_builder_config(di_builder, config)

    async with di_builder.enter_scope("app") as di_state:
        mediator = await di_builder.execute(init_mediator, "app", state=di_state)
        setup_mediator(mediator)

        app = init_api(mediator, di_builder, di_state, config.api.debug)
        await run_api(app, config.api)


if __name__ == "__main__":
    asyncio.run(main())
