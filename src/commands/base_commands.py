from src.commands.interfaces import BaseCommand


class MultiplyCommand(BaseCommand):

    def execute(self) -> float:
        return self._a * self._b


class DivideCommand(BaseCommand):

    def execute(self) -> float:
        return self._a / self._b


class SubtractCommand(BaseCommand):

    def execute(self) -> float:
        return self._a - self._b


class AddCommand(BaseCommand):

    def execute(self) -> float:
        return self._a + self._b


class ExponentialCommand(BaseCommand):

    def execute(self) -> float:
        return self._a ** self._b
