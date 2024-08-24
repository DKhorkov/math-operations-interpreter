import pytest

from src.config import MATH_COMMANDS, BASE_COMMANDS
from src.interpreter import MathOperationsInterpreter
from src.tokens_parser import TokensParser
from src.lexical_processor import LexicalProcessor


@pytest.fixture
def interpreter(lexical_processor: LexicalProcessor, tokens_parser: TokensParser) -> MathOperationsInterpreter:
    return MathOperationsInterpreter(
        interpreter_base_commands=BASE_COMMANDS,
        interpreter_math_commands=MATH_COMMANDS,
        parser=tokens_parser,
        lexical_processor=lexical_processor
    )


@pytest.fixture
def tokens_parser() -> TokensParser:
    return TokensParser()


@pytest.fixture
def lexical_processor() -> LexicalProcessor:
    return LexicalProcessor()
