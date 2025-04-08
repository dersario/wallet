from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class TypeOfTransaction(StrEnum):
    Send = "Send"
    Receive = "Receive"


class MakeTransactionSchema(BaseModel):
    # model_config = ConfigDict(from_attributes=True)
    sum: float
    receiver: str


class TransactionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    sum: float
    sender: str
    receiver: str
    date: datetime


class ResponseTransactionSchema(TransactionSchema):
    type: TypeOfTransaction
