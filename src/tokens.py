from dataclasses import dataclass

from src.enums import TokenTypesEnum


@dataclass
class Token:
    type: TokenTypesEnum
    literal: str

    def __str__(self) -> str:
        return f'{self.__class__.__name__}({self.type}, {self.literal})'
