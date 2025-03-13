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


@pytest.mark.parametrize("sql", (
    pytest.param("FROM table1 |> DROP col1", id="pipe_drop_single"),
    pytest.param("FROM table1 |> DROP col1,", id="pipe_drop_single_trailing_comma"),
    pytest.param("FROM table1 |> DROP col1, col2", id="pipe_drop_multi"),
))
def test_pipe_drop_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)


@pytest.mark.parametrize("sql", (
    pytest.param("FROM table1 |> RENAME col1 AS col2", id="pipe_rename_single"),
    pytest.param("FROM table1 |> RENAME col1 AS col2,", id="pipe_rename_single_trailing_comma"),
    pytest.param("FROM table1 |> RENAME col1 AS col2, col3 AS col4", id="pipe_rename_multi"),
))
def test_pipe_rename_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)


@pytest.mark.parametrize("sql", (
    pytest.param("FROM table1 |> RENAME col1.nested AS col2", id="pipe_rename_nested"),
))
def test_pipe_rename_error(sql, assert_parse_tree_error):
    assert_parse_tree_error(sql)


@pytest.mark.parametrize("sql", (
    pytest.param("FROM table1 |> AS table2", id="pipe_as_single"),
))
def test_as_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)


@pytest.mark.parametrize("sql", (
    pytest.param("FROM table1 |> WHERE col1", id="pipe_where_single"),
))
def test_where_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)
