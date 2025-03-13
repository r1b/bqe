from pathlib import Path
from lark import Lark
from .settings import PACKAGE_ROOT

GRAMMAR_ROOT = PACKAGE_ROOT / "grammar"
GRAMMAR_PATH = GRAMMAR_ROOT / "bqe.lark"
GRAMMAR_SOURCES = GRAMMAR_ROOT / "src"


def get_parser() -> Lark:
    return Lark(GRAMMAR_PATH.read_text(), import_paths=[GRAMMAR_SOURCES], parser='lalr')