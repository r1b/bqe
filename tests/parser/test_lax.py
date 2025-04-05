import pytest


@pytest.mark.parametrize(
    "sql",
    (
        pytest.param("a and b and c", id="lax_expr_and"),
        pytest.param("case when a and b then c else d end", id="lax_expr_case"),
        pytest.param("|> SELECT a, b, c", id="lax_expr_pipe_select"),
        pytest.param("|> AGGREGATE GROUP BY a, b, ROLLUP(c,d)", id="lax_expr_pipe_agg"),
    ),
)
def test_lax_ok(sql, assert_parse_tree):
    assert_parse_tree(sql, lax=True)
