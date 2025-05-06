import logging
import logging.config
from contextlib import asynccontextmanager
from typing import cast

import yaml
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from wallet.setup.db import DatabaseManager
from wallet.setup.exceptions import AppException, app_exception_handler
from wallet.setup.settings import AppSettings
from wallet.transactions.repositories import TransactionRepository
from wallet.transactions.routers import transactions_routers
from wallet.transactions.services import TransactionService
from wallet.users.repositories import UserRepository
from wallet.users.routers import users_routers
from wallet.users.services import UserService

logger = logging.getLogger(__name__)


def setup_app():
    with open("config.yaml") as config:
        c = yaml.load(config, yaml.FullLoader)
        logging.config.dictConfig(c)

    app = FastAPI(
        title="wallet",
        lifespan=app_lifetime,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

    app.include_router(transactions_routers)
    app.include_router(users_routers)

    app.add_exception_handler(AppException, app_exception_handler)

    settings = AppSettings()

    user_repository = UserRepository()
    transaction_reporitory = TransactionRepository()

    app.state.token_secret = settings.token_secret
    app.state.db_manager = DatabaseManager(settings.db_url)
    app.state.user_service = UserService(user_repository)
    app.state.transaction_service = TransactionService(transaction_reporitory)

    return app


@asynccontextmanager
async def app_lifetime(app: FastAPI):
    db_manager = cast(DatabaseManager, app.state.db_manager)

    logger.info("Starting")

    await db_manager.initialize()
    logger.info("Started")

    yield
    logger.info("Stopping app")
    await db_manager.dispose()
    logger.info("Stoped.")
