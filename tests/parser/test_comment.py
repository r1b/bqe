import pytest


@pytest.mark.parametrize(
    "sql",
    (
        pytest.param("-- myfile.sql\nSELECT 1", id="comment_sql_leading"),
        pytest.param("SELECT\n  1, -- one\n  2", id="comment_sql_expr"),
        pytest.param("SELECT 1\n-- one", id="comment_sql_trailing"),
        pytest.param("# TODO: SELECT 2\nSELECT 1", id="comment_sh_leading"),
        pytest.param("SELECT\n  1, # one\n  2", id="comment_sh_expr"),
        pytest.param("SELECT 1\n# one", id="comment_sh_trailing"),
        pytest.param("/* TODO: SELECT 2 */\nSELECT 1", id="comment_c_leading"),
        pytest.param("SELECT\n  1, /* one */\n  2", id="comment_c_expr"),
        pytest.param("SELECT 1\n/* one */", id="comment_c_trailing"),
    ),
)
def test_comment_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)
