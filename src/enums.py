from enum import Enum


class TokenTypesEnum(str, Enum):
    NUMBER = 'number'
    PLUS = 'plus'
    MINUS = 'minus'
    STAR = 'star'
    SLASH = 'slash'
    CARET = 'caret'
    LEFT_PARENTHESIS = 'left_parenthesis'
    RIGHT_PARENTHESIS = 'right_parenthesis'
    EOF = 'EOF'
