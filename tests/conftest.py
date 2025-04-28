import inspect

import pytest
from lark.exceptions import UnexpectedInput

from bqe.ast import pretty
from bqe.parser import parse, transform


@pytest.fixture
def assert_parse_tree(snapshot):
    def assert_parse_tree_impl(sql, lax=False, with_ast=False):
        tree = parse(sql, lax=lax)

        pretty_sql = inspect.cleandoc(sql)
        pretty_tree = tree.pretty().rstrip("\n")

        context = [pretty_sql, pretty_tree]

        if with_ast:
            # TODO: This is a temporary flag for incrementally building out the AST
            ast = transform(tree)
            context.append(pretty(ast, sql=sql))

        assert snapshot == "\n\n".join(context)

    return assert_parse_tree_impl


@pytest.fixture
def assert_parse_tree_error():
    def assert_parse_tree_impl(sql, *, expected_exception=None, match=None, lax=False):
        with pytest.raises(expected_exception or UnexpectedInput, match=match):
            parse(sql, lax=lax)

    return assert_parse_tree_impl
