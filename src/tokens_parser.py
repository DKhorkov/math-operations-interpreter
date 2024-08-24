from typing import List

from src.enums import TokenTypesEnum
from src.exceptions import ParseError
from src.config import OPERATIONS
from src.tokens import Token
from src.expressions import Expression, BinaryOperation, Number, UnaryOperation


class TokensParser:
    """
    Creates Abstract Syntax Tree according to operations priority in provided expression.

    program := computation
    computation := term ( (PLUS | MINUS) term )*
    term := unary ( (STAR | SLASH ) unary )*
    unary := PLUS unary | MINUS unary | exponentiation
    exponentiation := atom CARET unary | atom
    atom := LEFT_PARENTHESIS computation RIGHT_PARENTHESIS | number
    number := INT
    """

    def __init__(self) -> None:
        self._tokens: List[Token] = []
        self._next_token_index: int = 0

    def parse(self, tokens: List[Token]) -> Expression:
        """
        Parses the expression, created by user.
        """

        # initializes for each new parsing process:
        self._next_token_index = 0
        self._tokens = tokens

        computation: Expression = self._parse_computation()
        self._get_next_token(expected_token_type=TokenTypesEnum.EOF)
        return computation

    def _parse_computation(self) -> Expression:
        result: Expression = self._parse_term()
        while (next_token_type := self._get_next_token_type()) in {TokenTypesEnum.PLUS, TokenTypesEnum.MINUS}:
            operation: str = OPERATIONS[next_token_type]
            self._get_next_token(expected_token_type=next_token_type)
            right: Expression = self._parse_term()
            result = BinaryOperation(operation=operation, left=result, right=right)

        return result

    def _parse_term(self) -> Expression:
        """
        Parses an expression with multiplications and divisions.
        """

        result: Expression = self._parse_unary()
        while (next_token_type := self._get_next_token_type()) in {TokenTypesEnum.STAR, TokenTypesEnum.SLASH}:
            operation: str = OPERATIONS[next_token_type]
            self._get_next_token(expected_token_type=next_token_type)
            right: Expression = self._parse_unary()
            result = BinaryOperation(operation=operation, left=result, right=right)

        return result

    def _parse_unary(self) -> Expression:
        """
        Parses a unary operator.
        """

        if (next_token_type := self._get_next_token_type()) in {TokenTypesEnum.PLUS, TokenTypesEnum.MINUS}:
            operation: str = OPERATIONS[next_token_type]
            self._get_next_token(expected_token_type=next_token_type)
            expression: Expression = self._parse_unary()
            return UnaryOperation(operation=operation, expression=expression)
        else:  # No unary operators in sight.
            return self._parse_exponentiation()

    def _parse_exponentiation(self) -> Expression:
        """
        Parses a caret operator.
        """

        expression: Expression = self._parse_atom()
        next_token_type: TokenTypesEnum = self._get_next_token_type()
        if next_token_type == TokenTypesEnum.CARET:
            self._get_next_token(expected_token_type=TokenTypesEnum.CARET)
            right: Expression = self._parse_unary()
            expression = BinaryOperation(operation=OPERATIONS[next_token_type], left=expression, right=right)

        return expression

    def _parse_atom(self) -> Expression:
        """
        Parses a parenthesised expression or a number.
        """

        expression: Expression
        if self._get_next_token_type() == TokenTypesEnum.LEFT_PARENTHESIS:
            self._get_next_token(expected_token_type=TokenTypesEnum.LEFT_PARENTHESIS)
            expression = self._parse_computation()
            self._get_next_token(expected_token_type=TokenTypesEnum.RIGHT_PARENTHESIS)
        else:
            expression = self._parse_number()

        return expression

    def _parse_number(self) -> Number:
        return Number(float(self._get_next_token(expected_token_type=TokenTypesEnum.NUMBER).literal))

    def _get_next_token(self, expected_token_type: TokenTypesEnum) -> Token:
        """
        Returns the next token if it is of the expected type.

        In other case raises error.
        """

        next_token: Token = self._tokens[self._next_token_index]
        self._next_token_index += 1

        if next_token.type != expected_token_type:
            raise ParseError(f'Expected {expected_token_type}, but received {next_token!r}.')

        return next_token

    def _get_next_token_type(self) -> TokenTypesEnum:
        """
        Checks the type of upcoming token without consuming it.
        """

        return self._tokens[self._next_token_index].type
