import pytest


@pytest.mark.parametrize("sql", (
    pytest.param("(SELECT 1)", id="query_expr"),
    pytest.param("(SELECT (SELECT (SELECT 1)))", id="query_expr_nested"),
))
def test_query_expr_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)


@pytest.mark.parametrize("sql", (
    pytest.param("SELECT 1", id="select_literal"),
    pytest.param("SELECT column1 FROM table1", id="select_list_single"),
    pytest.param("SELECT column1, column2 FROM table1", id="select_list_multi"),
    pytest.param("SELECT column1 AS alias1 FROM table1", id="select_list_alias_explicit"),
    pytest.param("SELECT column1 alias1 FROM table1", id="select_list_alias_implicit"),
    pytest.param("SELECT column1, FROM table2", id="select_list_trailing_comma"),
    pytest.param("SELECT * FROM table1", id="select_star"),
    pytest.param("SELECT column1.* FROM table1", id="select_star_scoped"),
    pytest.param("SELECT column1.column2.* FROM table1", id="select_star_scoped_nested"),
    pytest.param("SELECT * EXCEPT (column1) FROM table1", id="select_star_except_single"),
    pytest.param("SELECT * EXCEPT (column1, column2) FROM table1", id="select_star_except_multi"),
    pytest.param("SELECT * REPLACE (column1 AS alias1) FROM table1", id="select_star_replace_single"),
    pytest.param("SELECT * REPLACE (column1 AS alias2, column2 AS alias2) FROM table1", id="select_star_replace_multi"),
    pytest.param("SELECT ALL column1 FROM table1", id="select_mode_all"),
    pytest.param("SELECT DISTINCT column1 FROM table1", id="select_mode_distinct"),
    pytest.param("SELECT column1, column2 FROM table1, table2", id="select_from_multi"),
    pytest.param("SELECT column1 FROM table1 AS alias1", id="select_from_alias_explicit"),
    pytest.param("SELECT column1 FROM table1 alias1", id="select_from_alias_implicit"),
    pytest.param("SELECT column1 FROM (SELECT column1 FROM table1)", id="select_from_subquery"),
    pytest.param("SELECT column1 FROM (SELECT column1 FROM table1) AS table2", id="select_from_subquery_aliased"),
))
def test_select_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)