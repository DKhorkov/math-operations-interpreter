from typing import Dict, Type

from src.commands import (
    BaseCommand,
    MathCommand,
    SinCommand,
    CosCommand,
    TanCommand,
    SqrtCommand,
    SubtractCommand,
    ExponentialCommand,
    AddCommand,
    ExpCommand,
    LogCommand,
    DivideCommand,
    MultiplyCommand
)
from src.enums import TokenTypesEnum


LEXICAL_RULES: Dict[TokenTypesEnum, str] = {
    TokenTypesEnum.NUMBER: r'(\d+(\.\d+)?)',
    TokenTypesEnum.PLUS: r'(\+)',
    TokenTypesEnum.MINUS: r'(\-)',
    TokenTypesEnum.STAR: r'(\*)',
    TokenTypesEnum.SLASH: r'(/)',
    TokenTypesEnum.CARET: r'(\^)',
    TokenTypesEnum.LEFT_PARENTHESIS: r'(\()',
    TokenTypesEnum.RIGHT_PARENTHESIS: r'(\))'
}

OPERATIONS: Dict[TokenTypesEnum, str] = {
    TokenTypesEnum.PLUS: '+',
    TokenTypesEnum.MINUS: '-',
    TokenTypesEnum.STAR: '*',
    TokenTypesEnum.SLASH: '/',
    TokenTypesEnum.CARET: '^',
}

BASE_COMMANDS: Dict[str, Type[BaseCommand]] = {
    '+': AddCommand,
    '-': SubtractCommand,
    '*': MultiplyCommand,
    '/': DivideCommand,
    '^': ExponentialCommand,
}

MATH_COMMANDS: Dict[str, Type[MathCommand]] = {
    'sin': SinCommand,
    'cos': CosCommand,
    'tan': TanCommand,
    'log': LogCommand,
    'exp': ExpCommand,
    'sqrt': SqrtCommand,
}

EXIT_VARIABLE: str = 'exit'
RESULT_VARIABLE: str = 'result'
