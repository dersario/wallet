from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column,relationship
import typing
from enum import StrEnum
from datetime import datetime

from wallet.setup.db import Base

class TypeOfTransaction(StrEnum):
    Send = "Send"
    Receive = "Receive"


class TransactionModel(Base):
    __tablename__="transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    sum: Mapped[float]
    date: Mapped[datetime]
    sender: Mapped[str]
    receiver: Mapped[str]

#    owner: Mapped["UserModel"] = relationship(cascade="save-update", back_populates="transactions")


