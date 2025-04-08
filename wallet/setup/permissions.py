from abc import ABC, abstractmethod

from wallet.users.models import UserModel


class BasePermission(ABC):
    @abstractmethod
    def check_permission(self, account: UserModel | None):
        pass


class Authenticated(BasePermission):
    def check_permission(self, account):
        return account is not None


class Anonymous(BasePermission):
    def check_permission(self, account):
        return account is None
