class CustomException(Exception):
    msg: str

    def __str__(self) -> str:
        return self.msg


class ExpressionSyntaxError(CustomException):

    def __init__(self) -> None:
        self.msg: str = (
            'В выражении допущена синтаксическая ошибка! '
            'Пожалуйста, проверьте входные данные и попробуйте снова!\n'
        )


class ParseError(CustomException):

    def __init__(self, msg: str) -> None:
        self.msg: str = msg


class IncorrectVariableAssignmentError(CustomException):

    def __init__(self) -> None:
        self.msg: str = (
            'Некорректные входные данные. '
            'Входные данные должны иметь следующий вид: "var = expression"\n'
        )


class UnknownExpressionTypeError(CustomException):

    def __init__(self) -> None:
        self.msg: str = 'Получен неизвестный тип выражения\n'
