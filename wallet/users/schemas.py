from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    balance: float


class RegisterUserSchema(BaseModel):
    name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    password: Annotated[str, StringConstraints(min_length=8)]
