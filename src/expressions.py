from dataclasses import dataclass


@dataclass
class TreeNode:
    pass


@dataclass
class Expression(TreeNode):
    pass


@dataclass
class UnaryOperation(Expression):
    """ - (2 + 3), where minus is operation and (2 + 3) is an expression"""
    operation: str
    expression: Expression


@dataclass
class BinaryOperation(Expression):
    operation: str
    left: Expression
    right: Expression


@dataclass
class Number(Expression):
    value: float
