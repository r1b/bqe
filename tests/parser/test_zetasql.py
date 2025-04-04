# Tests from zetasql
# Ref: https://github.com/google/zetasql/tree/2025.03.1/zetasql/parser/testdata
import pytest


# https://github.com/google/zetasql/blob/2025.03.1/zetasql/parser/testdata/pipe_aggregate.test
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
    ),
)
def test_pipe_agg(sql, assert_parse_tree):
    assert_parse_tree(sql)
