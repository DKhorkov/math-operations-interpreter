import math

from src.commands.interfaces import MathCommand


class SqrtCommand(MathCommand):

    def execute(self) -> float:
        return math.sqrt(self._value)


class SinCommand(MathCommand):

    def execute(self) -> float:
        return math.sin(self._value)


class CosCommand(MathCommand):

    def execute(self) -> float:
        return math.cos(self._value)


class LogCommand(MathCommand):

    def execute(self) -> float:
        return math.log(self._value)


class TanCommand(MathCommand):

    def execute(self) -> float:
        return math.tan(self._value)


class ExpCommand(MathCommand):

    def execute(self) -> float:
        return math.exp(self._value)
