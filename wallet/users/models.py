import typing

from sqlalchemy.orm import Mapped, mapped_column

from wallet.setup.db import Base

if typing.TYPE_CHECKING:
    pass


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    balance: Mapped[float]
    password: Mapped[str]


#    transactions: Mapped[list["TransactionModel"]] = relationship(cascade="save-update", back_populates="owner")
