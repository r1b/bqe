from pathlib import Path
from lark import Lark
from .settings import PACKAGE_ROOT

GRAMMAR_ROOT = PACKAGE_ROOT / "grammar"
GRAMMAR_PATH = GRAMMAR_ROOT / "bqe.lark"


def get_parser() -> Lark:
    return Lark(GRAMMAR_PATH.read_text(), parser='lalr')