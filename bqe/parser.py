import logging
from lark import Lark, logger as lark_logger
from lark.exceptions import UnexpectedInput

from .settings import BQE_DEBUG, PACKAGE_ROOT
from .transformer import AstTransformer, ParserTransformer


if BQE_DEBUG:
    lark_logger.setLevel(logging.DEBUG)

GRAMMAR_PATH = PACKAGE_ROOT / "grammar" / "bqe.lark"

parser = Lark(
    GRAMMAR_PATH.read_text(),
    parser="lalr",
    start=["start_query", "start_pipe", "start_expr"],
    debug=BQE_DEBUG,
    propagate_positions=True,
)

parser_transformer = ParserTransformer()
ast_transformer = AstTransformer()


def transform(tree):
    return ast_transformer.transform(tree)


def parse(sql: str, *, lax=False):
    """Parse SQL. If `lax` is `True`, attempt to parse multiple forms."""
    tree = parse_lax(sql) if lax else parse_strict(sql)
    tree = parser_transformer.transform(tree)
    return tree


def parse_strict(sql: str):
    """Parse a SQL statement or script."""
    return parser.parse(sql, start="start_query")


def parse_lax(sql: str):
    """Iteratively tries to parse SQL as:
    - A statement or script (identical to `parse_strict`)
    - A pipe expression
    - A column expression
    """
    try:
        return parse_strict(sql)
    except UnexpectedInput:
        pass

    try:
        return parser.parse(sql, start="start_pipe")
    except UnexpectedInput:
        pass

    return parser.parse(sql, start="start_expr")
