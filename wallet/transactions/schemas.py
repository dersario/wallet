from datetime import datetime
from pydantic import BaseModel, ConfigDict, StringConstraints
from typing import Annotated

class MakeTransactionSchema(BaseModel):
    #model_config = ConfigDict(from_attributes=True)
    sum: float
    receiver: str

class TransactionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    sum: float
    sender: str
    receiver: str
    date: datetime
