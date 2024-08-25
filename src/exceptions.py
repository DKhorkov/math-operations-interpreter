class CustomException(Exception):
    msg: str

    def __str__(self) -> str:
        return self.msg


class ExpressionSyntaxError(CustomException):

    def __init__(self) -> None:
        self.msg: str = 'There is a syntax error in the expression. Please check your input and try again.\n'


class ParseError(CustomException):

    def __init__(self, msg: str) -> None:
        self.msg: str = msg


class IncorrectVariableAssignmentError(CustomException):

    def __init__(self) -> None:
        self.msg: str = (
            'Invalid input data. Input data should look like this: "var = expression", '
            'where "var" contains only alphabetic characters.\n'
        )


class UnknownExpressionTypeError(CustomException):

    def __init__(self) -> None:
        self.msg: str = 'Unknown expression type received.\n'


class CustomZeroDivisionError(CustomException):

    def __init__(self) -> None:
        self.msg: str = 'Number can not be divided by zero. Please check your input and try again.\n'
