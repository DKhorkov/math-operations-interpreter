import os
import sys
from typing import Optional

# Adding ./src to python path for running from console purpose:
sys.path.append(os.getcwd())

from src.config import BASE_COMMANDS, MATH_COMMANDS, RESULT_VARIABLE, EXIT_VARIABLE
from src.interpreter import MathOperationsInterpreter
from src.lexical_processor import LexicalProcessor
from src.tokens_parser import TokensParser


if __name__ == '__main__':
    interpreter: MathOperationsInterpreter = MathOperationsInterpreter(
        interpreter_base_commands=BASE_COMMANDS,
        interpreter_math_commands=MATH_COMMANDS,
        parser=TokensParser(),
        lexical_processor=LexicalProcessor()
    )

    user_input: str = ''
    result: Optional[float] = None
    while not (result := interpreter.get_result()):
        user_input = input('>>: ').strip(' ').lower()
        if EXIT_VARIABLE in user_input:
            sys.exit(0)

        interpreter.interpret(user_input=user_input)

    print(f'{RESULT_VARIABLE} = {result}')
