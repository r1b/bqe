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


@pytest.mark.parametrize("sql", (
    pytest.param("FROM table1 |> LIMIT 1", id="pipe_limit_integer_literal"),
    pytest.param("FROM table1 |> LIMIT @limit", id="pipe_limit_param"),
    pytest.param("FROM table1 |> LIMIT 1 OFFSET 2", id="pipe_limit_offset"),
))
def test_limit_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)


@pytest.mark.parametrize("sql", (
    pytest.param("FROM table1 |> AGGREGATE SUM(col1)", id="pipe_agg_single"),
    pytest.param("FROM table1 |> AGGREGATE SUM(col1) AS col2", id="pipe_agg_single_alias"),
    pytest.param("FROM table1 |> AGGREGATE SUM(col1) AS col2, SUM(col3) AS col4", id="pipe_agg_multi_alias"),
    pytest.param("FROM table1 |> AGGREGATE SUM(col1) AS col2 GROUP BY col3", id="pipe_agg_group_by_single"),
    pytest.param("FROM table1 |> AGGREGATE SUM(col1) AS col2 GROUP BY col3 AS col4", id="pipe_agg_group_by_single_alias"),
    pytest.param("FROM table1 |> AGGREGATE SUM(col1) AS col2 GROUP BY col3 AS col4, col5 AS col6",
                 id="pipe_agg_group_by_multi_alias"),
    pytest.param("FROM table1 |> AGGREGATE SUM(col1) AS col2 GROUP BY ()",
                 id="pipe_agg_group_by_empty"),
    pytest.param("FROM table1 |> AGGREGATE SUM(col1) AS col2 GROUP BY ROLLUP (col3, col4)",
                 id="pipe_agg_group_by_rollup"),
    pytest.param("FROM table1 |> AGGREGATE SUM(col1) AS col2 GROUP BY CUBE (col3, (col4, col5))",
                 id="pipe_agg_group_by_cube"),
    pytest.param("FROM table1 |> AGGREGATE SUM(col1) AS col2 GROUP BY GROUPING SETS (col3, (col4, col5), col6)",
                 id="pipe_agg_group_by_grouping_sets"),
))
def test_agg_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)


@pytest.mark.parametrize("sql", (
    pytest.param("FROM table1 |> ORDER BY col1", id="order_by_single"),
    pytest.param("FROM table1 |> ORDER BY col1, col2", id="order_by_multi"),
    pytest.param("FROM table1 |> ORDER BY col1 ASC, col2 DESC", id="order_by_multi_sort"),
    pytest.param("FROM table1 |> ORDER BY col1 NULLS FIRST, col2 NULLS LAST", id="order_by_multi_nulls"),
    pytest.param("FROM table1 |> ORDER BY col1 ASC NULLS FIRST, col2 DESC NULLS LAST", id="order_by_multi_kitchen_sink"),
))
def test_order_by_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)


@pytest.mark.parametrize("sql", (
    pytest.param("FROM table1 |> UNION ALL (SELECT 1)", id="set_operation_all_single"),
    pytest.param("FROM table1 |> INTERSECT DISTINCT (SELECT 1), (SELECT 2)", id="set_operation_distinct_multi"),
    pytest.param("FROM table1 |> EXCEPT ALL BY NAME (SELECT 1 as col1)", id="set_operation_by_name"),
    pytest.param("FROM table1 |> UNION ALL CORRESPONDING (SELECT 1 as col1)", id="set_operation_corresponding"),
    pytest.param("FROM table1 |> UNION ALL STRICT CORRESPONDING (SELECT 1 as col1)", id="set_operation_strict_corresponding"),
    pytest.param("FROM table1 |> EXCEPT ALL BY NAME ON (col1) (SELECT 1 as col1)", id="set_operation_by_name_on_single"),
    pytest.param("FROM table1 |> EXCEPT ALL BY NAME ON (col1,col2) (SELECT 1 as col1)",
                 id="set_operation_by_name_on_multi"),
    pytest.param("FROM table1 |> EXCEPT ALL STRICT CORRESPONDING BY (col1) (SELECT 1 as col1)", id="set_operation_strict_corresponding_by"),
    pytest.param("FROM table1 |> FULL UNION ALL BY NAME (SELECT 1 as col1)",
                 id="set_operation_with_criteria_full"),
    pytest.param("FROM table1 |> LEFT UNION ALL BY NAME (SELECT 1 as col1)",
                 id="set_operation_with_criteria_left"),
    pytest.param("FROM table1 |> LEFT OUTER UNION ALL BY NAME (SELECT 1 as col1)",
                 id="set_operation_with_criteria_left_outer"),
    pytest.param("FROM table1 |> INNER UNION ALL BY NAME (SELECT 1 as col1)",
                 id="set_operation_with_criteria_inner"),
))
def test_set_operation_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)


@pytest.mark.parametrize("sql", (
    pytest.param("FROM table1 |> JOIN table2 USING (col1)", id="join_using_single"),
    pytest.param("FROM table1 |> JOIN table2 USING (col1, col2)", id="join_using_multi"),
    pytest.param("FROM table1 |> JOIN table2 ON col1 = col2", id="join_on_single_expr"),
    pytest.param("FROM table1 |> JOIN table2 ON col1 = col2 AND col3 != col4", id="join_on_compound_expr"),
    pytest.param("FROM table1 |> INNER JOIN table2 USING (col1)", id="join_inner"),
    pytest.param("FROM table1 |> LEFT JOIN table2 USING (col1)", id="join_left"),
    pytest.param("FROM table1 |> LEFT OUTER JOIN table2 USING (col1)", id="join_left_outer"),
    pytest.param("FROM table1 |> FULL JOIN table2 USING (col1)", id="join_full"),
    pytest.param("FROM table1 |> FULL OUTER JOIN table2 USING (col1)", id="join_full_outer"),
    pytest.param("FROM table1 |> RIGHT JOIN table2 USING (col1)", id="join_right"),
    pytest.param("FROM table1 |> RIGHT OUTER JOIN table2 USING (col1)", id="join_right_outer"),
    pytest.param("FROM table1 |> CROSS JOIN table2 USING (col1)", id="join_cross"),
))
def test_join_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)


@pytest.mark.parametrize("sql", (
    pytest.param("FROM table1 |> CALL APPENDS('1970-01-01')", id="call"),
    pytest.param("FROM table1 |> CALL APPENDS('1970-01-01') AS table2", id="call_alias_explicit"),
    pytest.param("FROM table1 |> CALL APPENDS('1970-01-01') table2", id="call_alias_implicit"),
))
def test_call_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)

@pytest.mark.parametrize("sql", (
    pytest.param("FROM table1 |> WINDOW SUM(col1) OVER ()", id="window_simple"),
    pytest.param("FROM table1 |> WINDOW SUM(col1) OVER (PARTITION BY col2)", id="window_partition_by_single"),
    pytest.param("FROM table1 |> WINDOW SUM(col1) OVER (PARTITION BY col2, col3)", id="window_partition_by_multi"),
    pytest.param("FROM table1 |> WINDOW SUM(col1) OVER (ORDER BY col2)", id="window_order_by_single"),
    pytest.param("FROM table1 |> WINDOW SUM(col1) OVER (ORDER BY col2, col3)", id="window_order_by_multi"),
    pytest.param("FROM table1 |> WINDOW SUM(col1) OVER (PARTITION BY col2 ORDER BY col3)", id="window_parition_and_order_by"),
    pytest.param("FROM table1 |> WINDOW SUM(col1) OVER (ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)",
                 id="window_frame_rows"),
    pytest.param("FROM table1 |> WINDOW SUM(col1) OVER (RANGE BETWEEN 1 PRECEDING AND 1 FOLLOWING)",
                 id="window_frame_range"),
))
def test_window_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)


@pytest.mark.parametrize("sql", (
    pytest.param("FROM table1 |> TABLESAMPLE SYSTEM (10 percent)", id="tablesample"),
))
def test_tablesample_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)


@pytest.mark.parametrize("sql", (
    pytest.param("FROM table1 |> PIVOT (SUM(col1) FOR quarter in ('Q1', 'Q2'))", id="pivot"),
    pytest.param("FROM table1 |> PIVOT (SUM(col1) FOR quarter in ('Q1', 'Q2')) AS col2", id="pivot_aliased"),
))
def test_pivot_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)


@pytest.mark.parametrize("sql", (
    pytest.param("FROM table1 |> UNPIVOT (col1 FOR quarter IN (q1, q2))", id="unpivot"),
    pytest.param("FROM table1 |> UNPIVOT (col1 FOR quarter IN (q1, q2)) AS col2", id="unpivot_aliased"),
))
def test_unpivot_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)
