from contextlib import asynccontextmanager
from typing import cast
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from wallet.setup.db import DatabaseManager
from wallet.setup.settings import AppSettings
from wallet.users.repositories import UserRepository
from wallet.users.services import UserService
from wallet.transactions.repositories import TransactionRepository
from wallet.transactions.services import TransactionService
from wallet.transactions.routers import transactions_routers
from wallet.users.routers import users_routers

def setup_app():
    app = FastAPI(
        title="wallet",
        lifespan=app_lifetime,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,)

    app.include_router(transactions_routers)
    app.include_router(users_routers)

    settings = AppSettings()

    user_repository = UserRepository()
    transaction_reporitory = TransactionRepository()

    app.state.db_manager = DatabaseManager(settings.db_url)
    app.state.user_service = UserService(user_repository)
    app.state.transaction_service = TransactionService(transaction_reporitory)
    
    return app

@asynccontextmanager
async def app_lifetime(app: FastAPI):
    db_manager = cast(DatabaseManager, app.state.db_manager)

    await db_manager.initialize()

    yield

    await db_manager.dispose()
    