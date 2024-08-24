from src.expressions import TreeNode, BinaryOperation, UnaryOperation, Number
from src.lexical_processor import LexicalProcessor
from src.tokens_parser import TokensParser


def test_tokens_parser_base_expression(tokens_parser: TokensParser, lexical_processor: LexicalProcessor) -> None:
    expression: str = '1 + 3'
    expected_tree: TreeNode = BinaryOperation(
        left=Number(value=1.0),
        operation='+',
        right=Number(value=3.0)
    )

    tree: TreeNode = tokens_parser.parse(lexical_processor.process_expression(expression=expression))
    assert expected_tree == tree


def test_tokens_parser_multipart_expression(tokens_parser: TokensParser, lexical_processor: LexicalProcessor) -> None:
    expression: str = '(1 + 2) ^ -3 / 5 * 2 + 2 ^ 3'
    expected_tree: TreeNode = BinaryOperation(
        left=BinaryOperation(
            left=BinaryOperation(
                left=BinaryOperation(
                    left=BinaryOperation(
                        left=Number(value=1.0),
                        operation='+',
                        right=Number(value=2.0)
                    ),
                    operation='^',
                    right=UnaryOperation(
                        operation='-',
                        expression=Number(value=3.0)
                    )
                ),
                operation='/',
                right=Number(value=5.0)
            ),
            operation='*',
            right=Number(value=2.0)
        ),
        operation='+',
        right=BinaryOperation(
            left=Number(value=2.0),
            operation='^',
            right=Number(value=3.0)
        )
    )

    tree: TreeNode = tokens_parser.parse(lexical_processor.process_expression(expression=expression))
    assert expected_tree == tree
