import pytest
from lark.exceptions import UnexpectedInput

from bqe.parser import get_parser


@pytest.fixture
def parser():
    return get_parser()


@pytest.fixture
def assert_parse_tree(parser, snapshot):
    def assert_parse_tree_impl(sql):
        tree = parser.parse(sql)
        assert snapshot == tree.pretty()
    return assert_parse_tree_impl


@pytest.fixture
def assert_parse_tree_error(parser, snapshot):
    def assert_parse_tree_impl(sql, *, expected_exception=None, match=None):
        with pytest.raises(expected_exception or UnexpectedInput, match=match):
            parser.parse(sql)
    return assert_parse_tree_impl
