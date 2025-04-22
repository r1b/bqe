import inspect

import pytest
from lark.exceptions import UnexpectedInput

from bqe.parser import parse


@pytest.fixture
def assert_parse_tree(snapshot):
    def assert_parse_tree_impl(sql, lax=False):
        tree = parse(sql, lax=lax)

        pretty_sql = inspect.cleandoc(sql)
        pretty_tree = tree.pretty()

        # Tree.pretty has trailing newlines
        assert snapshot == f"{pretty_sql}\n\n{pretty_tree}"

    return assert_parse_tree_impl


@pytest.fixture
def assert_parse_tree_error():
    def assert_parse_tree_impl(sql, *, expected_exception=None, match=None, lax=False):
        with pytest.raises(expected_exception or UnexpectedInput, match=match):
            parse(sql, lax=lax)

    return assert_parse_tree_impl
