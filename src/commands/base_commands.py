from src.commands.interfaces import BaseCommand
from src.exceptions import CustomZeroDivisionError


class MultiplyCommand(BaseCommand):

    def execute(self) -> float:
        return self._a * self._b


class DivideCommand(BaseCommand):

    def execute(self) -> float:
        try:
            return self._a / self._b
        except ZeroDivisionError:
            raise CustomZeroDivisionError()


class SubtractCommand(BaseCommand):

    def execute(self) -> float:
        return self._a - self._b


class AddCommand(BaseCommand):

    def execute(self) -> float:
        return self._a + self._b


class ExponentialCommand(BaseCommand):

    def execute(self) -> float:
        return self._a ** self._b
