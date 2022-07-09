#!/usr/bin/env python3
from dependency_injector.wiring import Provide, inject

from telegramfeed.container import Container


@inject
def main(subscription_service=Provide[Container.subscription_service]):
    subscription_service.listen_and_process()


if __name__ == "__main__":
    container = Container()
    container.config.db_connection_string.from_env("DB_CONNECTION_STRING")
    container.config.telegram_token.from_env("TELEGRAM_TOKEN")
    container.wire(modules=[__name__])

    main()
