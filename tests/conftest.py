import pytest

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