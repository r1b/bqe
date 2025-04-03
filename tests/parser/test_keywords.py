import pytest


@pytest.mark.parametrize(
    "sql",
    (
        pytest.param("SELECT date abc", id="select_kw_date_column"),
        pytest.param("SELECT abc date", id="select_kw_date_alias"),
        pytest.param("SELECT date date", id="select_kw_date_double"),
        pytest.param("SELECT format abc", id="select_kw_format_column"),
        pytest.param("SELECT abc format", id="select_kw_format_alias"),
        pytest.param("SELECT percent abc", id="select_kw_percent_column"),
        pytest.param("SELECT abc percent", id="select_kw_percent_alias"),
    ),
)
def test_nonreserved_keyword_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)
