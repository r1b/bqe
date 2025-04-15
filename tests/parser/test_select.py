import pytest


@pytest.mark.parametrize(
    "sql",
    (
        pytest.param("SELECT 1", id="select_literal"),
        pytest.param("SELECT column1 FROM table1", id="select_list_single"),
        pytest.param("SELECT column1, column2 FROM table1", id="select_list_multi"),
        pytest.param("SELECT column1 AS alias1 FROM table1", id="select_list_alias_explicit"),
        pytest.param("SELECT column1 alias1 FROM table1", id="select_list_alias_implicit"),
        pytest.param("SELECT column1, FROM table2", id="select_list_trailing_comma"),
        pytest.param("SELECT * FROM table1", id="select_star"),
        pytest.param("SELECT column1.* FROM table1", id="select_star_scoped"),
        pytest.param(
            "SELECT column1.column2.* FROM table1",
            id="select_star_scoped_nested",
        ),
        pytest.param("SELECT column1 FROM table1 AS alias1", id="select_from_alias_explicit"),
        pytest.param("SELECT column1 FROM table1 alias1", id="select_from_alias_implicit"),
        pytest.param(
            "SELECT column1 FROM table1 FOR SYSTEM_TIME AS OF '1970-01-01'",
            id="select_from_time_travel",
        ),
        pytest.param("SELECT AS STRUCT column1 FROM table1", id="select_as_struct"),
        pytest.param("SELECT AS VALUE column1 FROM table1", id="select_as_value"),
        pytest.param(
            """
            SELECT
                *,
                column1,
                (SELECT 1) AS column2
            FROM
                (SELECT column7 FROM table2) AS alias2
            """,
            id="select_subqueries",
        ),
        pytest.param(
            """
            SELECT DISTINCT column1 FROM table1
            """,
            id="select_distinct",
        ),
        pytest.param(
            """
            SELECT * EXCEPT(column1, column2) FROM table1
            """,
            id="select_star_except",
        ),
        pytest.param(
            """
            SELECT struct_column.* EXCEPT(column1, column2) FROM table1
            """,
            id="select_dot_star_except",
        ),
        pytest.param(
            """
            SELECT * REPLACE(1 AS column1, 2 AS column2) FROM table1
            """,
            id="select_star_replace",
        ),
        pytest.param(
            """
            SELECT struct_column.* REPLACE(1 AS column1, 2 AS column2) FROM table1
            """,
            id="select_dot_star_replace",
        ),
    ),
)
def test_select_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)


@pytest.mark.parametrize(
    "sql",
    (
        pytest.param("SELECT ,", id="select_comma_only"),
        pytest.param("SELECT ,1", id="select_comma_leading"),
        # FIXME: BQ says "Syntax error: SELECT list must not be empty at [1:8]"
        pytest.param(
            "SELECT from FROM table1", id="select_column_reserved_word", marks=pytest.mark.xfail
        ),
        pytest.param(
            "SELECT * REPLACE (column1 alias1) FROM table1", id="select_star_replace_alias_implicit"
        ),
    ),
)
def test_select_error(sql, assert_parse_tree_error):
    assert_parse_tree_error(sql)


@pytest.mark.parametrize(
    "sql",
    (
        pytest.param("(SELECT 1)", id="subquery"),
        pytest.param("(SELECT (SELECT (SELECT 1)))", id="subquery_nested"),
        pytest.param("SELECT column1 FROM (SELECT column1 FROM table1)", id="select_from_subquery"),
        pytest.param(
            "SELECT column1 FROM (SELECT column1 FROM table1) AS table2",
            id="select_from_subquery_aliased",
        ),
    ),
)
def test_subquery_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)


@pytest.mark.parametrize(
    "sql",
    (
        pytest.param("SELECT column1 FROM UNNEST(array1)", id="unnest"),
        pytest.param("SELECT column1 FROM UNNEST(array1) AS alias1", id="unnest_alias"),
        pytest.param(
            "SELECT column1 FROM UNNEST(array1) WITH OFFSET",
            id="unnest_with_offset",
        ),
        pytest.param(
            "SELECT column1 FROM UNNEST(array1) WITH OFFSET AS alias1",
            id="unnest_with_offset_alias",
        ),
        pytest.param(
            "SELECT column1 FROM UNNEST(array1) AS alias1 WITH OFFSET AS alias2",
            id="unnest_alias_with_offset_alias",
        ),
    ),
)
def test_unnest_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)
