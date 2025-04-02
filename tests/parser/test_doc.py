# Tests for queries in the documentation
# Ref: https://cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax
import pytest


@pytest.mark.parametrize(
    "sql",
    (
        pytest.param(
            """
            FROM Produce
            |> WHERE
                item != 'bananas'
                AND category IN ('fruit', 'nut')
            |> AGGREGATE COUNT(*) AS num_items, SUM(sales) AS total_sales
                GROUP BY item
            |> ORDER BY item DESC;
            """,
            id="doc_query_comparison",
        ),
        pytest.param(
            """
            FROM Produce
            |> AS p1
            |> JOIN Produce AS p2 USING (item)
            |> WHERE item = 'bananas'
            |> SELECT p1.item, p2.sales;
            """,
            id="doc_from",
        ),
        pytest.param(
            """
            FROM (SELECT 'apples' AS item, 2 AS sales)
            |> SELECT item AS fruit_name;
            """,
            id="doc_select",
        ),
        pytest.param(
            """
            (SELECT 'apples' AS item, 2 AS sales)
            |> UNION ALL (SELECT 'carrots' AS item, 8 AS sales)
            |> EXTEND item IN ('carrots', 'oranges') AS is_orange;
            """,
            id="doc_extend",
        ),
    ),
)
def test_doc_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)
