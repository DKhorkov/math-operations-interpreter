from abc import abstractmethod, ABC


class BaseCommand(ABC):

    def __init__(self, a: float, b: float) -> None:
        self._a: float = a
        self._b: float = b

    @abstractmethod
    def execute(self) -> float:
        raise NotImplementedError


class MathCommand(ABC):

    def __init__(self, value: float) -> None:
        self._value: float = value

    @abstractmethod
    def execute(self) -> float:
        raise NotImplementedError
