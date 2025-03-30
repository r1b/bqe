import pytest
from lark.exceptions import UnexpectedInput

from bqe.parser import parse


@pytest.fixture
def assert_parse_tree(snapshot):
    def assert_parse_tree_impl(sql):
        tree = parse(sql)
        assert snapshot == tree.pretty()
    return assert_parse_tree_impl


@pytest.fixture
def assert_parse_tree_error():
    def assert_parse_tree_impl(sql, *, expected_exception=None, match=None):
        with pytest.raises(expected_exception or UnexpectedInput, match=match):
            parse(sql)
    return assert_parse_tree_impl
