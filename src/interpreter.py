from typing import Type, Dict, List, Tuple, Optional

from src.commands import BaseCommand, MathCommand
from src.config import RESULT_VARIABLE
from src.exceptions import (
    IncorrectVariableAssignmentError,
    UnknownExpressionTypeError,
    ParseError,
    ExpressionSyntaxError,
    CustomZeroDivisionError
)
from src.expressions import TreeNode, UnaryOperation, BinaryOperation, Number
from src.interfaces import Processor, Parser
from src.tokens import Token


class MathOperationsInterpreter:

    def __init__(
            self,
            interpreter_base_commands: Dict[str, Type[BaseCommand]],
            interpreter_math_commands: Dict[str, Type[MathCommand]],
            parser: Parser,
            lexical_processor: Processor
    ) -> None:

        self._base_commands: Dict[str, Type[BaseCommand]] = interpreter_base_commands
        self._math_commands: Dict[str, Type[MathCommand]] = interpreter_math_commands
        self._parser: Parser = parser
        self._lexical_processor: Processor = lexical_processor

        # Storage for executed expressions, which can be user in future expressions:
        self._user_variables: Dict[str, float] = {}

    def interpret(self, user_input: str) -> None:
        """
        1) Receives user input and checks it validity;
        2) Interprets the expression in the user input and executes it;
        3) Assigns executed result of the expression to a given variable.
        """

        try:
            key: str
            expression: str
            key, expression = self._validate_user_input(user_input=user_input.lower())

            expression_result: float = self._execute(expression=expression)
            self._user_variables[key] = expression_result
        except (
                ParseError,
                ExpressionSyntaxError,
                IncorrectVariableAssignmentError,
                UnknownExpressionTypeError,
                CustomZeroDivisionError
        ) as e:
            print(e)

    def _validate_user_input(self, user_input: str) -> Tuple[str, str]:
        """
        Validates user input. If input is invalid, raises IncorrectVariableAssignmentError.

        User input must contain a variable, an assignment sign, and an assignment expression.
        Variable must contain only alphabetic characters.

        Examples of correct user input are:
        1) "x = 2";
        2) "x= 2";
        3) "x=2";
        """

        user_input_sep: str = ' '
        values: List[str] = user_input.split(user_input_sep)

        # Check, if input is "variable = expression":
        user_variable: str
        expression: str
        equal_sign: str = '='
        if values[0].endswith(equal_sign):
            user_variable = values[0][: -1]  # Variable name without "=" symbol
            expression = user_input_sep.join(values[1:])
        elif len(values) == 1 and equal_sign in values[0]:
            use_var_index: int = values[0].find(equal_sign)
            user_variable = values[0][: use_var_index]
            expression = values[0][use_var_index + 1:]
        elif values[1] == equal_sign:
            user_variable = values[0]
            expression = user_input_sep.join(values[2:])
        else:
            raise IncorrectVariableAssignmentError()

        if not user_variable.isalpha():
            raise IncorrectVariableAssignmentError()

        expression = self._substitute_user_variables(expression=expression)
        return user_variable, expression

    def _substitute_user_variables(self, expression: str) -> str:
        """
        Substitutes already interpreted variable in expression if exists.
        """

        for key in self._user_variables.keys():
            if key in expression:
                expression = expression.replace(key, str(self._user_variables[key]))

        return expression

    def _execute(self, expression: str) -> float:
        """
        1) All basic mathematical functions, such as sin, cos, tan, log, sqrt and exp,
        are executed if any in the expression;
        2) Generates tokens from the expression for parsing purpose;
        3) Creates AST (Abstract Syntax Tree) on tokens basis;
        4) Recursively calculates the value of a parsed expression based on the AST.
        """

        expression = self._execute_math_operations(expression=expression)
        tokens: List[Token] = self._lexical_processor.process_expression(expression=expression)

        try:
            operations_tree: TreeNode = self._parser.parse(tokens=tokens)
        except ParseError:
            raise ExpressionSyntaxError()

        return self._calculate_node_value(node=operations_tree)

    def _execute_math_operations(self, expression: str) -> str:
        """
        Searches for a math function in expression.
        If such function is found, calculates its value and replaces the subexpression related to the
        math function with the calculated value.

        Example:
        :param expression: "sqrt(25) + 5 * 2"
        :return: "5.0 + 5 * 2"
        """

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
        """
        Extracts subexpression from parentless in original expression for math functions purposes.
        If original expression is not valid or there is no parentless in it, raises ExpressionSyntaxError.
        Returns extracted subexpression and the remaining part of original expression.

        Example:
        :param expression: "(5 + 2) * 3"
        :return: ("5 + 2", " * 3")
        """

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
        """
        1) Gets an AST tree node, which is one of next types: UnaryOperation, BinaryOperation or Number;
        2) If node is a Number type - returns it, else recursively calculates expression, stored in node.
        """

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
        """
        Returns the value for a result variable if it exists.

        This variable signals that all expressions have been interpreted and variable storage is no longer required.
        """

        result: Optional[float] = self._user_variables.get(RESULT_VARIABLE)
        if result:
            self._user_variables.clear()

        return result
