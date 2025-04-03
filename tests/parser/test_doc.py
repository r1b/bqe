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
        pytest.param(
            """
            (SELECT 'apples' AS item, 2 AS sales)
            |> UNION ALL (SELECT 'bananas' AS item, 5 AS sales)
            |> UNION ALL (SELECT 'carrots' AS item, 8 AS sales)
            |> EXTEND SUM(sales) OVER() AS total_sales;
            """,
            id="doc_extend_window",
        ),
        pytest.param(
            """
            FROM Produce
            |> EXTEND SUM(sales) OVER item_window AS category_total
               WINDOW item_window AS (PARTITION BY category);
            """,
            id="doc_extend_named_window",
        ),
        pytest.param(
            """
            (SELECT 1 AS x, 11 AS y)
            |> UNION ALL (SELECT 2 AS x, 22 AS y)
            |> SET x = x * x, y = 3;
            """,
            id="doc_set",
        ),
        pytest.param(
            """
            FROM (SELECT 2 AS x, 3 AS y) AS t
            |> SET x = x * x, y = 8
            |> SELECT t.x AS original_x, x, y;
            """,
            id="doc_set_nested",
        ),
        pytest.param(
            """
            SELECT 'apples' AS item, 2 AS sales, 'fruit' AS category
            |> DROP sales, category;
            """,
            id="doc_drop",
        ),
        pytest.param(
            """
            FROM (SELECT 1 AS x, 2 AS y) AS t
            |> DROP x
            |> SELECT t.x AS original_x, y;
            """,
            id="doc_drop_nested",
        ),
        pytest.param(
            """
            SELECT 1 AS x, 2 AS y, 3 AS z
            |> AS t
            |> RENAME y AS renamed_y
            |> SELECT *, t.y AS t_y;
            """,
            id="doc_rename",
        ),
        pytest.param(
            """
            (
                SELECT "000123" AS id, "apples" AS item, 2 AS sales
                |> UNION ALL (SELECT "000456" AS id, "bananas" AS item, 5 AS sales)
            ) AS sales_table
            |> AGGREGATE SUM(sales) AS total_sales GROUP BY id, item
            -- The sales_table alias is now out of scope. We must introduce a new one.
            |> AS t1
            |> JOIN (SELECT 456 AS id, "yellow" AS color) AS t2
               ON CAST(t1.id AS INT64) = t2.id
            |> SELECT t2.id, total_sales, color;
            """,
            id="doc_as",
        ),
    ),
)
def test_doc_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)
