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
