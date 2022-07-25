import sqlalchemy
from dependency_injector import containers, providers
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Connectable

from telegramfeed import repositories, services


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    engine = providers.Singleton(create_engine, config.db_connection_string)

    subscription_repo = providers.Singleton(
        repositories.SubscriptionRepo, engine=engine
    )

    telegram_service = providers.Singleton(
        services.TelegramService, config.telegram_token
    )

    subscription_service = providers.Singleton(
        services.SubscriptionService,
        telegram=telegram_service,
        subscription_repo=subscription_repo,
    )
