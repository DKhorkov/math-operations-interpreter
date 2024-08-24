from typing import List

import pytest

from src.exceptions import ExpressionSyntaxError
from src.lexical_processor import LexicalProcessor
from src.tokens import Token
from src.enums import TokenTypesEnum


def test_lexical_processor_process_base_expression(lexical_processor: LexicalProcessor) -> None:
    expression: str = '5 + 2'
    expected_tokens: List[Token] = [
        Token(type=TokenTypesEnum.NUMBER, literal='5'),
        Token(type=TokenTypesEnum.PLUS, literal='+'),
        Token(type=TokenTypesEnum.NUMBER, literal='2'),
        Token(type=TokenTypesEnum.EOF, literal=''),
    ]

    tokens: List[Token] = lexical_processor.process_expression(expression=expression)
    assert expected_tokens == tokens


def test_lexical_processor_process_multipart_expression(lexical_processor: LexicalProcessor) -> None:
    expression: str = '(5 + 2) * (-3)'
    expected_tokens: List[Token] = [
        Token(type=TokenTypesEnum.LEFT_PARENTHESIS, literal='('),
        Token(type=TokenTypesEnum.NUMBER, literal='5'),
        Token(type=TokenTypesEnum.PLUS, literal='+'),
        Token(type=TokenTypesEnum.NUMBER, literal='2'),
        Token(type=TokenTypesEnum.RIGHT_PARENTHESIS, literal=')'),
        Token(type=TokenTypesEnum.STAR, literal='*'),
        Token(type=TokenTypesEnum.LEFT_PARENTHESIS, literal='('),
        Token(type=TokenTypesEnum.MINUS, literal='-'),
        Token(type=TokenTypesEnum.NUMBER, literal='3'),
        Token(type=TokenTypesEnum.RIGHT_PARENTHESIS, literal=')'),
        Token(type=TokenTypesEnum.EOF, literal=''),
    ]

    tokens: List[Token] = lexical_processor.process_expression(expression=expression)
    assert expected_tokens == tokens


def test_lexical_processor_expression_fail_due_syntax_error(lexical_processor: LexicalProcessor) -> None:
    with pytest.raises(ExpressionSyntaxError):
        expression: str = '(5 + 2)a'
        lexical_processor.process_expression(expression=expression)
