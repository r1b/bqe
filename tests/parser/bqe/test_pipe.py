import pytest

@pytest.mark.parametrize("sql", (
    pytest.param("FROM table1", id="pipe_from"),
    pytest.param("FROM table1 |> SELECT col1", id="pipe_from_select"),
    pytest.param("SELECT col1 FROM table1 |> SELECT col1", id="pipe_select_select"),
    pytest.param("(SELECT col1 FROM table1) |> SELECT col1", id="pipe_subquery_select"),
))
def test_pipe_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)


@pytest.mark.parametrize("sql", (
    pytest.param("FROM table1 | > SELECT col1", id="pipe_with_space"),
))
def test_pipe_error(sql, assert_parse_tree_error):
    assert_parse_tree_error(sql)


@pytest.mark.parametrize("sql", (
    pytest.param("FROM table1 |> EXTEND POW(col1, 2)", id="pipe_extend_single"),
    pytest.param("FROM table1 |> EXTEND POW(col1, 2),", id="pipe_extend_single_trailing_comma"),
    pytest.param("FROM table1 |> EXTEND POW(col1, 2) AS col2", id="pipe_extend_single_alias"),
    pytest.param("FROM table1 |> EXTEND POW(col1, 2) AS col2, EXP(col1, 2)", id="pipe_extend_multi"),
))
def test_pipe_extend_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)


@pytest.mark.parametrize("sql", (
    pytest.param("FROM table1 |> SET col1 = POW(col1, 2)", id="pipe_set_single"),
    pytest.param("FROM table1 |> SET col1 = POW(col1, 2),", id="pipe_set_single_trailing_comma"),
    pytest.param("FROM table1 |> SET col1 = POW(col1, 2), col2 = EXP(col1, 2)", id="pipe_set_multi"),
))
def test_pipe_set_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)
