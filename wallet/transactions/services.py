from datetime import date, datetime

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from wallet.setup.auth import AuthenticatedAccount
from wallet.setup.dependencies import UserServiceDep
from wallet.transactions.models import TransactionModel
from wallet.transactions.repositories import TransactionRepository
from wallet.transactions.schemas import MakeTransactionSchema, ResponseTransactionSchema
from wallet.users.schemas import UserSchema

# from wallet.setup.dependencies import UserServiceDep


class TransactionService:
    def __init__(self, repository: TransactionRepository):
        self.__repository = repository

    async def create_transaction(
        self,
        sender: UserSchema,
        schema: MakeTransactionSchema,
        session: AsyncSession,
        service: UserServiceDep,
    ):
        transaction = TransactionModel(
            date=datetime.now(),
            sum=schema.sum,
            receiver=schema.receiver,
            sender=sender.name,
        )
        receiver = await service.find_by_name(schema.receiver, session)
        if receiver.name == sender.name:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail="Не пытайтесь отправить деньги самому себе",
            )
        if receiver is None:
            raise HTTPException(
                status.HTTP_409_CONFLICT, detail="Получателя не существует"
            )
        await service.update_balance(sender.id, receiver, schema.sum, session)
        session.add(transaction)
        await session.commit()

        return transaction

    async def find_by_id(self, id: int, session: AsyncSession):
        transaction = await session.get(TransactionModel, id)
        if transaction in None:
            raise HTTPException(status.HTTP_409_CONFLICT)
        return transaction

    async def get_of_period(
        self,
        date_1: date,
        date_2: date,
        current_user: AuthenticatedAccount,
        session: AsyncSession,
    ):
        transactions: set[TransactionModel] = set(
            await self.__repository.get_all_by_sender(current_user.name, session)
        )
        transactions.update(
            (await self.__repository.get_all_by_receiver(current_user.name, session))
        )
        t: list[ResponseTransactionSchema] = []
        for i in transactions:
            date = i.date.date()
            if date > date_1 and date < date_2:
                if i.sender == current_user.name:
                    new_i = ResponseTransactionSchema(
                        sum=i.sum,
                        sender=i.sender,
                        receiver=i.receiver,
                        date=i.date,
                        type="Send",
                    )

                else:
                    new_i = ResponseTransactionSchema(
                        sum=i.sum,
                        sender=i.sender,
                        receiver=i.receiver,
                        date=i.date,
                        type="Receive",
                    )
                t.append(new_i)
        return t
