from lark import Lark
from lark.exceptions import UnexpectedInput

from .settings import PACKAGE_ROOT
from .transformer import BqeTransformer

GRAMMAR_PATH = PACKAGE_ROOT / "grammar" / "bqe.lark"

parser = Lark(
    GRAMMAR_PATH.read_text(),
    parser="lalr",
    start=["start_query", "start_pipe", "start_expr"],
)
transformer = BqeTransformer()


def parse(sql: str, *, lax=False):
    """Parse SQL. If `lax` is `True`, attempt to parse multiple forms."""
    tree = parse_lax(sql) if lax else parse_strict(sql)
    tree = transformer.transform(tree)
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
