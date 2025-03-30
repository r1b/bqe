import pytest


@pytest.mark.parametrize(
    "sql",
    (
        pytest.param("SELECT col1 FROM table1;", id="script_single"),
        pytest.param("SELECT col1 FROM table1; SELECT col2 FROM table2", id="script_multi"),
        pytest.param(
            "SELECT col1 FROM table1; SELECT col2 FROM table2;",
            id="script_multi_with_trailing_semi",
        ),
        pytest.param("FROM table1;", id="script_top_level_from"),
    ),
)
def test_script_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)
