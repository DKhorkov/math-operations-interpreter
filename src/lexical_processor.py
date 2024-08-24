import re
from typing import List, Optional

from src.enums import TokenTypesEnum
from src.exceptions import ExpressionSyntaxError
from src.tokens import Token
from src.config import LEXICAL_RULES


class LexicalProcessor:

    def __init__(self) -> None:
        self._expression: str = ''
        self._results: List[Token] = []

    def process_expression(self, expression: str) -> List[Token]:
        # initializes for each new expression processing:
        self._expression = expression
        self._results = []

        self._extract_regex_pattern_from_expression()

        # Добавляем токен, символизирующий окончание строки для дальнейших операций над предобработанным выражением:
        self._results.append(
            Token(
                literal='',
                type=TokenTypesEnum.EOF
            )
        )

        return self._results

    def _extract_regex_pattern_from_expression(self) -> None:
        while len(self._expression) > 0:
            max_rule: TokenTypesEnum = TokenTypesEnum.EOF
            max_lit: str = ''
            self._expression = self._expression.strip()

            # Ищем самую длинную часть выражения с помощью regex:
            for rule in LEXICAL_RULES.keys():
                regex_pattern: re.Pattern[str] = re.compile(pattern=LEXICAL_RULES[rule])
                regex_match: Optional[re.Match[str]] = regex_pattern.match(string=self._expression)
                if (regex_match is not None) and (len(regex_match.group(0)) > len(max_lit)):
                    max_lit = regex_match.group(0)
                    max_rule = rule

            if max_rule == TokenTypesEnum.EOF:
                raise ExpressionSyntaxError()

            self._expression = self._expression[len(max_lit):]  # Уменьшаем выражение на обработанную часть
            self._results.append(
                Token(
                    literal=max_lit,
                    type=max_rule
                )
            )