from lark import Lark

from .settings import PACKAGE_ROOT
from .transformer import BqeTransformer

GRAMMAR_PATH = PACKAGE_ROOT / "grammar" / "bqe.lark"

parser = Lark(GRAMMAR_PATH.read_text(), parser="lalr")
transformer = BqeTransformer()


def parse(sql: str):
    tree = parser.parse(sql)
    tree = transformer.transform(tree)
    return tree
