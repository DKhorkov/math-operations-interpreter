from dataclasses import dataclass


@dataclass
class TreeNode:
    """
    Abstract Syntax Tree.
    """

    pass


@dataclass
class Expression(TreeNode):
    pass


@dataclass
class UnaryOperation(Expression):
    """
    -(2 + 3), where minus is operation and (2 + 3) is an expression.
    """

    operation: str
    expression: Expression


@dataclass
class BinaryOperation(Expression):
    """
    1 * 2 + 3 * 3, where "1 * 2" is left expression, "+" is operation and "3 * 3" is right expression.
    """

    operation: str
    left: Expression
    right: Expression


@dataclass
class Number(Expression):
    value: float
