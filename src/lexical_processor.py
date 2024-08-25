import re
from typing import List, Optional

from src.enums import TokenTypesEnum
from src.exceptions import ExpressionSyntaxError
from src.interfaces import Processor
from src.tokens import Token
from src.config import LEXICAL_RULES


class LexicalProcessor(Processor):

    def __init__(self) -> None:
        self._expression: str = ''
        self._results: List[Token] = []

    def process_expression(self, expression: str) -> List[Token]:
        """
        Processes an expression and returns the resulting tokens, if the expression is valid.
        """

        # Initializes for each new expression processing:
        self._expression = expression
        self._results = []

        self._extract_regex_pattern_from_expression()

        # Add a token symbolizing the end of the line for further operations on the preprocessed expression:
        self._results.append(
            Token(
                literal='',
                type=TokenTypesEnum.EOF
            )
        )

        return self._results

    def _extract_regex_pattern_from_expression(self) -> None:
        """
        Extracts the regular expression pattern from the expression, starting from the beginning.
        If one of the regular expression patterns is found in the expression, the corresponding token will be created.
        In other case, expression is not valid and ExpressionSyntaxError will be raised.

        After the token is created, the expression is reduced by the characters used for tokenization
        and processed recursively.
        """

        while len(self._expression) > 0:
            max_rule: TokenTypesEnum = TokenTypesEnum.EOF
            max_lit: str = ''
            self._expression = self._expression.strip()

            # Finding the longest part of an expression using RegEx:
            for rule in LEXICAL_RULES.keys():
                regex_pattern: re.Pattern[str] = re.compile(pattern=LEXICAL_RULES[rule])
                regex_match: Optional[re.Match[str]] = regex_pattern.match(string=self._expression)
                if (regex_match is not None) and (len(regex_match.group(0)) > len(max_lit)):
                    max_lit = regex_match.group(0)
                    max_rule = rule

            if max_rule == TokenTypesEnum.EOF:
                raise ExpressionSyntaxError()

            self._expression = self._expression[len(max_lit):]  # Reduce the expression by the processed part
            self._results.append(
                Token(
                    literal=max_lit,
                    type=max_rule
                )
            )
