from abc import ABC, abstractmethod
from typing import List

from src.expressions import Expression
from src.tokens import Token


class Parser(ABC):

    @abstractmethod
    def parse(self, tokens: List[Token]) -> Expression:
        raise NotImplementedError


class Processor(ABC):

    @abstractmethod
    def process_expression(self, expression: str) -> List[Token]:
        raise NotImplementedError
