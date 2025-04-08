from typing import Annotated

from fastapi import Depends, Request

from wallet.transactions.services import TransactionService


def transaction_service(request: Request):
    return request.app.state.transaction_service


TransactionServiceDep = Annotated[TransactionService, Depends(transaction_service)]
