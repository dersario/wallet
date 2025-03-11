from datetime import date,datetime
from fastapi import APIRouter, Depends
from wallet.setup.dependencies import SessionDep, UserServiceDep
from wallet.transactions.dependencies import TransactionServiceDep
from wallet.setup.permissions import Anonymous, Authenticated
from wallet.setup.auth import AuthorizedAccount, AuthenticatedAccount
from wallet.transactions.schemas import MakeTransactionSchema, ResponseTransactionSchema, TransactionSchema


transactions_routers = APIRouter(prefix="/transactions", tags=["Транзакции"])

@transactions_routers.post("", summary="Совершить транзакцию", dependencies=[Depends(AuthorizedAccount(Authenticated()))])
async def make_transaction(
    schema: MakeTransactionSchema,
    sender: AuthenticatedAccount,
    Tservice: TransactionServiceDep,
    Uservice: UserServiceDep,
    session: SessionDep,
) -> TransactionSchema:
    transaction = await Tservice.create_transaction(sender, schema, session, Uservice)

    return TransactionSchema.model_validate(transaction)

@transactions_routers.get("")
async def get_transactions_of_period(
    session:SessionDep,
    current_user:AuthenticatedAccount,
    service:TransactionServiceDep,
    date1: date = date(2025,2,10),
    date2: date = date(2025,3,16),
) -> list[ResponseTransactionSchema]:
    return await service.get_of_period(date1,date2,current_user, session)