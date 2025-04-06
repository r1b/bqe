# Tests from zetasql
# Ref: https://github.com/google/zetasql/tree/2025.03.1/zetasql/parser/testdata
import pytest


# https://github.com/google/zetasql/blob/2025.03.1/zetasql/parser/testdata/pipe_aggregate.test
# https://github.com/google/zetasql/blob/2025.03.1/zetasql/parser/testdata/pipe_aggregate_group_by_aliases.test
# https://github.com/google/zetasql/blob/2025.03.1/zetasql/parser/testdata/pipe_aggregate_with_order.test
@pytest.mark.parametrize(
    "sql",
    (
        pytest.param(
            """
            select 1 x
            |> AGGREGATE count(*), sum(x) as xx
            """,
            id="zeta_pipe_agg",
        ),
        pytest.param(
            """
            select 1
            |> AGGREGATE sum(z), 1+count(x+1) GROUP BY x, y+2, 3
            """,
            id="zeta_pipe_agg_group_by",
        ),
        pytest.param(
            """
            select 1
            |> AGGREGATE 1, x, sum(y) OVER ()
            """,
            id="zeta_pipe_agg_window_fail_analysis",
        ),
        pytest.param(
            """
            select 1
            |> AGGREGATE sum(y) GROUP BY ()
            |> AGGREGATE sum(y) GROUP BY y, (), x
            """,
            id="zeta_pipe_agg_group_by_empty",
        ),
        pytest.param(
            """
            select 1
            |> AGGREGATE count(*) GROUP BY ROLLUP(x,y)
            |> AGGREGATE GROUP BY GROUPING SETS ((x), (y,z))
            |> AGGREGATE xyz GROUP BY GROUPING SETS(CUBE(x,y), (z,z), ROLLUP(a,b));
            """,
            id="zeta_pipe_agg_grouping_item_kitchen_sink",
        ),
        pytest.param(
            """
            select 1
            |> AGGREGATE count(*) as x, count(*) z
            """,
            id="zeta_pipe_agg_aliases",
        ),
        pytest.param(
            """
            select 1
            |> AGGREGATE count(*),
            |> AGGREGATE count(*), GROUP BY x
            """,
            id="zeta_pipe_agg_agg_list_trailing_comma",
        ),
        pytest.param(
            """
            select 1
            |> AGGREGATE GROUP BY x,
            |> AGGREGATE GROUP BY x, y,
            """,
            id="zeta_pipe_agg_group_by_trailing_comma",
        ),
        pytest.param(
            """
            select 1
            |> AGGREGATE x, s.*, f(y).*, (a+b).*
            """,
            id="zeta_pipe_agg_dot_star",
        ),
        pytest.param(
            """
            select 1
            |> AGGREGATE x.* except (a,b),
                         y.* replace (abc as def),
                         z.* except (a) replace (1+2 as ccc)
            """,
            id="zeta_pipe_agg_except_replace",
            marks=pytest.mark.xfail,
        ),
        pytest.param(
            """
            select 1
            |> AGGREGATE count(*) as x, count(*) z
               GROUP BY x AS y, z, 1 AS one, x+y AS xy
            """,
            id="zeta_pipe_agg_group_by_alias_explicit",
        ),
        pytest.param(
            """
            select 1
            |> AGGREGATE count(*) as x, count(*) z
               GROUP BY x y, x+y xy
            """,
            id="zeta_pipe_agg_group_by_alias_implicit",
        ),
        pytest.param(
            """
            select 1
            |> AGGREGATE
               GROUP BY
                  x,
                  x+1 ASC,
                  f() DESC,
                  z ASC NULLS FIRST,
                  zz DESC NULLS LAST,
                  a NULLS FIRST,
                  aa NULLS LAST
            """,
            id="zeta_pipe_agg_group_by_order_by_implicit",
        ),
        pytest.param(
            """
            select 1
            |> AGGREGATE 1 GROUP AND ORDER BY x, y DESC,
            """,
            id="zeta_pipe_agg_group_and_order_by",
        ),
        pytest.param(
            """
            select 1
            |> AGGREGATE 1
               GROUP AND ORDER BY (),ROLLUP(x),CUBE(x),GROUPING SETS(x)
            """,
            id="zeta_pipe_agg_group_and_order_by_grouping_sets_kitchen_sink",
        ),
        pytest.param(
            """
            from x
            |> AGGREGATE
               GROUP AND ORDER BY x+1 AS y ASC
            """,
            id="zeta_pipe_agg_group_and_order_by_aliased",
        ),
        pytest.param(
            """
            from t
            |> aggregate count(*) ASC,
               sum(x) alias DESC,
               avg(y) AS alias ASC NULLS FIRST,
               max(distinct z) DESC NULLS LAST,
               nosuffix()
            """,
            id="zeta_pipe_agg_order_by",
        ),
        pytest.param(
            """
            from t
            |> aggregate count(*) asc
               group by key asc
            """,
            id="zeta_pipe_agg_order_by_everywhere",
        ),
    ),
)
def test_pipe_agg(sql, assert_parse_tree):
    assert_parse_tree(sql)


@pytest.mark.parametrize(
    "sql",
    (
        pytest.param(
            """
            SELECT 1 |> AS t
            """,
            id="zeta_pipe_as",
        ),
        pytest.param(
            """
            SELECT 1 x |> AS t
            """,
            id="zeta_pipe_as_input_aliased",
        ),
        pytest.param(
            """
            SELECT 1 |> AS t1 |> AS t2;
            """,
            id="zeta_pipe_as_chained",
        ),
        pytest.param(
            """
            FROM (SELECT 1 AS a |> AS t)
            |> SELECT t.a
            """,
            id="zeta_pipe_as_scope_oopsie",
        ),
        pytest.param(
            """
            FROM t1
            |> JOIN t2 USING(key)
            |> AS t3
            """,
            id="zeta_pipe_as_typical_usage_join",
        ),
    ),
)
def test_pipe_as(sql, assert_parse_tree):
    assert_parse_tree(sql)


@pytest.mark.parametrize(
    "sql",
    (
        pytest.param(
            """
            select 1
            |> call f()
            |> call a.b.c(1, x.y, g(), named=>5)
            # TODO: TVF-specific syntax
            # |> call f(TABLE t, (select 1))
            # |> call f(DESCRIPTOR(col))
            # |> call f(MODEL m, CONNECTION c)
            """,
            id="zeta_pipe_call",
        ),
    ),
)
def test_pipe_call(sql, assert_parse_tree):
    assert_parse_tree(sql)


@pytest.mark.parametrize(
    "sql",
    (
        pytest.param(
            """
            select x
            |> drop a
            |> drop a,
            |> drop a,b,c
            |> drop a,b,c,
            """,
            id="zeta_pipe_drop",
        ),
    ),
)
def test_pipe_drop(sql, assert_parse_tree):
    assert_parse_tree(sql)


@pytest.mark.parametrize(
    "sql",
    (
        pytest.param(
            """
            from t
            """,
            id="zeta_pipe_from",
        ),
        pytest.param(
            """
            from unnest([1]) x
            """,
            id="zeta_pipe_from_unnest_aliased",
        ),
        pytest.param(
            """
            from (select * from t)
            """,
            id="zeta_pipe_from_subquery",
        ),
        pytest.param(
            """
            select (from t), EXISTS(from t1), ARRAY(from t2)
            from (from t)
            """,
            id="zeta_pipe_from_expression_subquery",
        ),
        pytest.param(
            """
            from tvf(1,2)
            """,
            id="zeta_pipe_from_tvf",
            marks=pytest.mark.xfail,
        ),
        pytest.param(
            """
            select * from tvf((from t))
            """,
            id="zeta_pipe_from_tvf_subquery",
            marks=pytest.mark.xfail,
        ),
        pytest.param(
            """
            from
              t1,
              t2 PIVOT(SUM(a) FOR b IN (0, 1)),
              t3 UNPIVOT (a FOR c IN (x, y)),
              t4 WITH OFFSET AS o
                 FOR SYSTEM TIME AS OF y
                 TABLESAMPLE SYSTEM(5 percent)
            """,
            id="zeta_pipe_from_postfix",
            marks=pytest.mark.xfail,
        ),
    ),
)
def test_pipe_from(sql, assert_parse_tree):
    assert_parse_tree(sql)


@pytest.mark.parametrize(
    "sql",
    (
        pytest.param(
            """
            select 1 x
            |> join t2.x.y
            |> join t3 using (x)
            |> left join t4 on true
            |> inner join (select zzz from zzz)
            |> cross join t6
            # Private syntax
            # |> natural join t7
            # |> hash join t7
            # |> lookup join t7
            """,
            id="zeta_pipe_join",
        ),
        pytest.param(
            """
            select 1 x
            # TODO: Add TVFs
            # |> join tvf((select 1))
            |> join unnest(y)
            |> join unnest(y.z) i WITH OFFSET o
            """,
            id="zeta_pipe_join_unnest",
        ),
    ),
)
def test_pipe_join(sql, assert_parse_tree):
    assert_parse_tree(sql)


@pytest.mark.parametrize(
    "sql",
    (
        pytest.param(
            """
            from t
            |> select sum(x) over(w), count(*) over (w2)
               window w AS (),
                      w2 AS (partition by a)
            |> extend max(y) over (w partition by x)
               window w AS (ORDER BY b ROWS CURRENT ROW)
            """,
            id="zeta_pipe_named_window",
        ),
        pytest.param(
            """
            from t
            |> select sum(x)
               window w AS ()
            """,
            id="zeta_pipe_named_window_unused",
        ),
        pytest.param(
            """
            from t
            |> select sum(x) over (w),
            window w AS (),
            """,
            id="zeta_pipe_named_window_select_trailing_comma",
        ),
        pytest.param(
            """
            from t
            |> extend sum(x) over (w),
            window w AS (),
            """,
            id="zeta_pipe_named_window_extend_trailing_comma",
        ),
    ),
)
def test_pipe_named_window(sql, assert_parse_tree):
    assert_parse_tree(sql)


@pytest.mark.parametrize(
    "sql",
    (
        pytest.param(
            """
            select 1
            |> order by x
            |> order by 1, x, y, x+1, sum(x), x() OVER ()
            |> order by x ASC, y DESC
            # |> order by x COLLATE "abc"
            |> order by x NULLS FIRST
            # |> order by x COLLATE "abc" ASC NULLS LAST
            """,
            id="zeta_pipe_order_by",
        ),
        pytest.param(
            """
            select 1
            |> order by x,
            |> order by x, y,
            """,
            id="zeta_pipe_order_by_trailing_comma",
        ),
    ),
)
def test_pipe_order_by(sql, assert_parse_tree):
    assert_parse_tree(sql)


@pytest.mark.parametrize(
    "sql",
    (
        pytest.param(
            """
            FROM t
            |> PIVOT(SUM(a) FOR b IN (0, 1))
            """,
            id="zeta_pipe_pivot_single",
        ),
        pytest.param(
            """
            FROM t
            |> PIVOT(SUM(a), SUM(b) FOR b IN (0)) pivot_table
            """,
            id="zeta_pipe_pivot_multi_implicit_alias",
        ),
        pytest.param(
            """
            FROM t
            |> PIVOT(SUM(a) AS sum_a, SUM(aa) sum_aa, 2+COUNT(b+3)
                     FOR t.x IN (z, x+y xpy, 1 AS one)) AS p
            """,
            id="zeta_pipe_pivot_aliased_exprs_kitchen_sink",
        ),
        pytest.param(
            """
            FROM t
            |> PIVOT(a FOR b IN (c)) AS PIVOT
            """,
            id="zeta_pipe_pivot_nonreserved_kw",
        ),
    ),
)
def test_pipe_pivot(sql, assert_parse_tree):
    assert_parse_tree(sql)
