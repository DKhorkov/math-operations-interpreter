from typing import Type, Dict, List, Tuple, Optional

from src.commands import BaseCommand, MathCommand
from src.config import RESULT_VARIABLE
from src.exceptions import (
    IncorrectVariableAssignmentError,
    UnknownExpressionTypeError,
    ParseError,
    ExpressionSyntaxError
)
from src.expressions import TreeNode, UnaryOperation, BinaryOperation, Number
from src.lexical_processor import LexicalProcessor
from src.tokens import Token
from src.tokens_parser import TokensParser


class MathOperationsInterpreter:

    def __init__(
            self,
            interpreter_base_commands: Dict[str, Type[BaseCommand]],
            interpreter_math_commands: Dict[str, Type[MathCommand]],
            parser: TokensParser,
            lexical_processor: LexicalProcessor
    ) -> None:

        self._base_commands: Dict[str, Type[BaseCommand]] = interpreter_base_commands
        self._math_commands: Dict[str, Type[MathCommand]] = interpreter_math_commands
        self._parser: TokensParser = parser
        self._lexical_processor: LexicalProcessor = lexical_processor

        self._user_vars: Dict[str, float] = {}

    def interpret(self, user_input: str) -> None:
        try:
            key: str
            expression: str
            key, expression = self._validate_user_input(user_input=user_input.lower())

            expression_result: float = self._execute(expression=expression)
            self._user_vars[key] = expression_result
        except (ParseError, ExpressionSyntaxError, IncorrectVariableAssignmentError, UnknownExpressionTypeError) as e:
            print(e)
        except ZeroDivisionError:
            print('Нельзя делить на ноль. Пожалуйста, попробуйте снова, используя корректные входные данные\n')

    def _validate_user_input(self, user_input: str) -> Tuple[str, str]:
        user_input_sep: str = ' '
        values: List[str] = user_input.split(user_input_sep)

        # Check, if input is "variable = expression":
        user_var: str
        expression: str
        equal_sign: str = '='
        if values[0].endswith(equal_sign):
            user_var = values[0][: -1]  # Variable name without "=" symbol
            expression = user_input_sep.join(values[1:])
        elif len(values) == 1 and equal_sign in values[0]:
            use_var_index: int = values[0].find(equal_sign)
            user_var = values[0][: use_var_index]
            expression = values[0][use_var_index + 1:]
        elif values[1] == equal_sign:
            user_var = values[0]
            expression = user_input_sep.join(values[2:])
        else:
            raise IncorrectVariableAssignmentError()

        # Check, if an already interpreted variable in expression:
        for key in self._user_vars.keys():
            if key in expression:
                expression = expression.replace(key, str(self._user_vars[key]))

        return user_var, expression

    def _execute(self, expression: str) -> float:
        expression = self._execute_math_operations(expression=expression)
        tokens: List[Token] = self._lexical_processor.process_expression(expression=expression)
        operations_tree: TreeNode = self._parser.parse(tokens=tokens)
        return self._calculate_node_value(node=operations_tree)

    def _execute_math_operations(self, expression: str) -> str:
        for math_command in self._math_commands.keys():
            math_command_index: int = expression.find(math_command)
            if math_command_index != -1:  # Not found
                math_command_expression: str
                postfix: str
                math_command_expression, postfix = self._extract_expression_from_parentless(
                    expression=expression[math_command_index + len(math_command):]
                )

                command = self._math_commands[math_command](
                    value=self._execute(
                        expression=math_command_expression
                    )
                )

                prefix: str = expression[: math_command_index]
                expression = prefix + str(command.execute()) + postfix

        return expression

    @staticmethod
    def _extract_expression_from_parentless(expression: str) -> Tuple[str, str]:
        opening_parenthesis: str = '('
        closing_parenthesis: str = ')'
        if not expression.startswith(opening_parenthesis):
            raise ExpressionSyntaxError()

        # Starting from -1, because it's index and will be straightaway incremented
        # at first iteration of for loop below:
        parentless_expression_end_index: int = -1

        parentless_stack: List[str] = []
        for index in range(len(expression)):
            parentless_expression_end_index += 1
            symbol: str = expression[index]
            if symbol == opening_parenthesis:
                parentless_stack.append(symbol)
            elif symbol == closing_parenthesis:
                parentless_stack.pop(0)

            if len(parentless_stack) == 0:
                break

        if len(parentless_stack) != 0:
            raise ExpressionSyntaxError()

        # Expression and postfix should be without parentless from original expression:
        parentless_expression: str = expression[1: parentless_expression_end_index]
        postfix: str = expression[parentless_expression_end_index + 1:]
        return parentless_expression, postfix

    def _calculate_node_value(self, node: TreeNode) -> float:
        command: BaseCommand
        if isinstance(node, UnaryOperation):
            command = self._base_commands[node.operation](
                a=0,  # Unary operation has only one part of expression
                b=self._calculate_node_value(node=node.expression)
            )

            return command.execute()
        elif isinstance(node, BinaryOperation):
            command = self._base_commands[node.operation](
                a=self._calculate_node_value(node=node.left),
                b=self._calculate_node_value(node=node.right)
            )

            return command.execute()
        elif isinstance(node, Number):
            return node.value
        else:
            raise UnknownExpressionTypeError()

    def get_result(self) -> Optional[float]:
        return self._user_vars.get(RESULT_VARIABLE)
