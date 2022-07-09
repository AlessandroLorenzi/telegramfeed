import pytest

from telegramfeed.container import Container


@pytest.fixture
def container() -> Container:
    container = Container()
    container.config.db_connection_string.from_env("DB_CONNECTION_STRING")
    container.config.telegram_token.from_env("TELEGRAM_TOKEN")
    container.wire(modules=[__name__])
    return container
