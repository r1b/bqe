from pathlib import Path
from lark import Lark
from .settings import PACKAGE_ROOT

GRAMMAR_PATH = PACKAGE_ROOT / Path("grammar/bigquery.lark")


def get_parser() -> Lark:
    return Lark(GRAMMAR_PATH.read_text(), parser='lalr')