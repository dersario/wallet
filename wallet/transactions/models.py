from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from wallet.setup.db import Base


class TransactionModel(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    sum: Mapped[float]
    date: Mapped[datetime]
    sender: Mapped[str]
    receiver: Mapped[str]


#    owner: Mapped["UserModel"] = relationship(cascade="save-update", back_populates="transactions")
