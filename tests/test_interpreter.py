import pytest

from src.config import OPERATIONS
from src.enums import TokenTypesEnum
from src.exceptions import (
    IncorrectVariableAssignmentError,
    ExpressionSyntaxError,
    UnknownExpressionTypeError
)
from src.expressions import (
    Expression,
    Number,
    BinaryOperation,
    UnaryOperation
)
from src.interpreter import MathOperationsInterpreter


def test_base_add(interpreter: MathOperationsInterpreter) -> None:
    interpreter.interpret(user_input='result = 5 + 4')
    assert interpreter.get_result() == 9.0


def test_base_subtract(interpreter: MathOperationsInterpreter) -> None:
    interpreter.interpret(user_input='result = 12 - 4')
    assert interpreter.get_result() == 8.0


def test_base_multiply(interpreter: MathOperationsInterpreter) -> None:
    interpreter.interpret(user_input='result = 2 * 4')
    assert interpreter.get_result() == 8.0


def test_base_divide(interpreter: MathOperationsInterpreter) -> None:
    interpreter.interpret(user_input='result = 10 / 5')
    assert interpreter.get_result() == 2.0


def test_base_exponent(interpreter: MathOperationsInterpreter) -> None:
    interpreter.interpret(user_input='result = 2 ^ 4')
    assert interpreter.get_result() == 16.0


def test_operations_priority(interpreter: MathOperationsInterpreter) -> None:
    interpreter.interpret(user_input='result = 4 * 5 + 10')
    assert interpreter.get_result() == 30.0


def test_parentless(interpreter: MathOperationsInterpreter) -> None:
    interpreter.interpret(user_input='result = (12 - 4) / 2')
    assert interpreter.get_result() == 4.0


def test_float_values(interpreter: MathOperationsInterpreter) -> None:
    interpreter.interpret(user_input='result = 13.00 + 12.00')
    assert interpreter.get_result() == 25.0


def test_variable_and_equal_sign_as_single_word(interpreter: MathOperationsInterpreter) -> None:
    interpreter.interpret(user_input='result= 13 * 2')
    assert interpreter.get_result() == 26.0


def test_expression_without_whitespaces(interpreter: MathOperationsInterpreter) -> None:
    interpreter.interpret(user_input='result=13.00+12.00')
    assert interpreter.get_result() == 25.0


def test_expression_with_negative_values(interpreter: MathOperationsInterpreter) -> None:
    interpreter.interpret(user_input='result = -13.00 + 12.00')
    assert interpreter.get_result() == -1.0


def test_expression_with_decimal_places(interpreter: MathOperationsInterpreter) -> None:
    interpreter.interpret(user_input='result = 13.22 + 1')
    assert interpreter.get_result() == 14.22


def test_variable_assignment(interpreter: MathOperationsInterpreter) -> None:
    interpreter.interpret(user_input='x = 5 * 2')
    interpreter.interpret(user_input='y = 3 + 20')
    interpreter.interpret(user_input='result = y - x * 4')
    assert interpreter.get_result() == -17.0


def test_negative_values(interpreter: MathOperationsInterpreter) -> None:
    interpreter.interpret(user_input='result = -13 + 5 * 2')
    assert interpreter.get_result() == -3.0


def test_negative_values_with_parentless(interpreter: MathOperationsInterpreter) -> None:
    interpreter.interpret(user_input='result = (-13) * (6 + 4.0)')
    assert interpreter.get_result() == -130.0


def test_variables_with_parentless(interpreter: MathOperationsInterpreter) -> None:
    interpreter.interpret(user_input='x = 5 * 2')
    interpreter.interpret(user_input='y = 2')
    interpreter.interpret(user_input='result = (x - 5) ^ y')
    assert interpreter.get_result() == 25.0


def test_base_sin(interpreter: MathOperationsInterpreter) -> None:
    interpreter.interpret(user_input='result = sin(5)')
    assert interpreter.get_result() == -0.9589242746631385


def test_base_cos(interpreter: MathOperationsInterpreter) -> None:
    interpreter.interpret(user_input='result = cos(10)')
    assert interpreter.get_result() == -0.8390715290764524


def test_base_tan(interpreter: MathOperationsInterpreter) -> None:
    interpreter.interpret(user_input='result = tan(1)')
    assert interpreter.get_result() == 1.5574077246549023


def test_base_log(interpreter: MathOperationsInterpreter) -> None:
    interpreter.interpret(user_input='result = log(2)')
    assert interpreter.get_result() == 0.6931471805599453


def test_base_exp(interpreter: MathOperationsInterpreter) -> None:
    interpreter.interpret(user_input='result = exp(7)')
    assert interpreter.get_result() == 1096.6331584284585


def test_base_sqrt(interpreter: MathOperationsInterpreter) -> None:
    interpreter.interpret(user_input='result = sqrt(4)')
    assert interpreter.get_result() == 2.0


def test_math_operations_with_base_operations(interpreter: MathOperationsInterpreter) -> None:
    interpreter.interpret(user_input='result = sin(0) * 2 + 3')
    assert interpreter.get_result() == 3.0


def test_math_operations_with_base_operations_and_parentless(interpreter: MathOperationsInterpreter) -> None:
    interpreter.interpret(user_input='result = sin(0) * (2 + 3)')
    assert interpreter.get_result() == 0.0


def test_math_operations_with_multipart_base_operations(interpreter: MathOperationsInterpreter) -> None:
    interpreter.interpret(user_input='result = sqrt(5 * (2 + 3))')
    assert interpreter.get_result() == 5.0


def test_math_operations_with_multipart_base_operations_and_parentless(interpreter: MathOperationsInterpreter) -> None:
    interpreter.interpret(user_input='result = 5 + sqrt(4 * (3 + 6 - 5)) ^ 2')
    assert interpreter.get_result() == 21.0


def test_math_operations_with_variables_and_with_parentless(interpreter: MathOperationsInterpreter) -> None:
    interpreter.interpret(user_input='x = sin(0)')
    interpreter.interpret(user_input='y = sqrt((9 - 5) * 4)')
    interpreter.interpret(user_input='result = (x + 2) ^ y')
    assert interpreter.get_result() == 16.0


def test_user_vars_is_empty_after_getting_result(interpreter: MathOperationsInterpreter) -> None:
    interpreter.interpret(user_input='result = 2 + 3')
    interpreter.get_result()
    assert len(interpreter._user_variables) == 0


def test_validate_user_input(interpreter: MathOperationsInterpreter) -> None:
    assert interpreter._validate_user_input(user_input='x = 3') == ('x', '3')


def test_validate_user_input_variable_and_equal_sign_as_single_word(interpreter: MathOperationsInterpreter) -> None:
    assert interpreter._validate_user_input(user_input='x= 3 * 2') == ('x', '3 * 2')


def test_validate_user_input_single_word(interpreter: MathOperationsInterpreter) -> None:
    assert interpreter._validate_user_input(user_input='x=3*2-1') == ('x', '3*2-1')


def test_validate_user_input_no_variable(interpreter: MathOperationsInterpreter) -> None:
    with pytest.raises(IncorrectVariableAssignmentError):
        interpreter._validate_user_input(user_input='3 + 2')


def test_validate_user_input_variable_is_numeric(interpreter: MathOperationsInterpreter) -> None:
    with pytest.raises(IncorrectVariableAssignmentError):
        interpreter._validate_user_input(user_input='3 = 2')


def test_substitute_user_variables(interpreter: MathOperationsInterpreter) -> None:
    interpreter.interpret(user_input='x = 2 + 3')
    expression = interpreter._substitute_user_variables(expression='result = x + 2')
    assert expression == 'result = 5.0 + 2'


def test_extract_expression_from_parentless(interpreter: MathOperationsInterpreter) -> None:
    assert interpreter._extract_expression_from_parentless(expression='(x + 2) - 4') == ('x + 2', ' - 4')


def test_extract_expression_from_parentless_with_no_parentless(interpreter: MathOperationsInterpreter) -> None:
    with pytest.raises(ExpressionSyntaxError):
        interpreter._extract_expression_from_parentless(expression='x * 5 -2')


def test_extract_expression_from_parentless_with_only_left_parentless(interpreter: MathOperationsInterpreter) -> None:
    with pytest.raises(ExpressionSyntaxError):
        interpreter._extract_expression_from_parentless(expression='(x * 5 -2')


def test_extract_expression_from_parentless_with_only_right_parentless(interpreter: MathOperationsInterpreter) -> None:
    with pytest.raises(ExpressionSyntaxError):
        interpreter._extract_expression_from_parentless(expression='x * 5) -2')


def test_execute_math_operations(interpreter: MathOperationsInterpreter) -> None:
    expression: str = interpreter._execute_math_operations(expression='sqrt(25)')
    assert expression == '5.0'


def test_execute_math_operations_incorrect_syntax(interpreter: MathOperationsInterpreter) -> None:
    with pytest.raises(ExpressionSyntaxError):
        interpreter._execute_math_operations(expression='sin28')


def test_calculate_binary_node_value(interpreter: MathOperationsInterpreter) -> None:
    value: float = interpreter._calculate_node_value(
        node=BinaryOperation(
            left=Number(value=3.0),
            operation=OPERATIONS[TokenTypesEnum.STAR],
            right=Number(value=2.0)
        )
    )

    assert value == 6.0


def test_calculate_plus_unary_node_value(interpreter: MathOperationsInterpreter) -> None:
    value: float = interpreter._calculate_node_value(
        node=UnaryOperation(
            operation=OPERATIONS[TokenTypesEnum.PLUS],
            expression=Number(4)
        )
    )

    assert value == 4.0


def test_calculate_minus_unary_node_value(interpreter: MathOperationsInterpreter) -> None:
    value: float = interpreter._calculate_node_value(
        node=UnaryOperation(
            operation=OPERATIONS[TokenTypesEnum.MINUS],
            expression=Number(3)
        )
    )

    assert value == -3.0


def test_calculate_number_node_value(interpreter: MathOperationsInterpreter) -> None:
    value: float = interpreter._calculate_node_value(
        node=Number(value=5)
    )

    assert value == 5.0


def test_calculate_node_value_with_incorrect_node_type(interpreter: MathOperationsInterpreter) -> None:
    with pytest.raises(UnknownExpressionTypeError):
        interpreter._calculate_node_value(node=Expression())
