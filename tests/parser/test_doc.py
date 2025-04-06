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
            FROM Produce AS p1
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
            (
                SELECT 'apples' AS item, 2 AS sales
                UNION ALL
                SELECT 'carrots' AS item, 8 AS sales
            )
            |> EXTEND item IN ('carrots', 'oranges') AS is_orange;
            """,
            id="doc_extend",
        ),
        pytest.param(
            """
            (
                SELECT 'apples' AS item, 2 AS sales
                UNION ALL
                SELECT 'bananas' AS item, 5 AS sales
                UNION ALL
                SELECT 'carrots' AS item, 8 AS sales
            )
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
            (
                SELECT 1 AS x, 11 AS y
                UNION ALL
                SELECT 2 AS x, 22 AS y
            )
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
                UNION ALL
                SELECT "000456" AS id, "bananas" AS item, 5 AS sales
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
        pytest.param(
            """
            (
                SELECT 'apples' AS item, 2 AS sales
                UNION ALL
                SELECT 'bananas' AS item, 5 AS sales
                UNION ALL
                SELECT 'carrots' AS item, 8 AS sales
            )
            |> WHERE sales >= 3;
            """,
            id="doc_where",
        ),
        pytest.param(
            """
            (
                SELECT 'apples' AS item, 2 AS sales
                UNION ALL
                SELECT 'bananas' AS item, 5 AS sales
                UNION ALL
                SELECT 'carrots' AS item, 8 AS sales
            )
            |> ORDER BY item
            |> LIMIT 1;
            """,
            id="doc_limit",
        ),
        pytest.param(
            """
            (
                SELECT 'apples' AS item, 2 AS sales
                UNION ALL
                SELECT 'bananas' AS item, 5 AS sales
                UNION ALL
                SELECT 'carrots' AS item, 8 AS sales
            )
            |> ORDER BY item
            |> LIMIT 1 OFFSET 2;
            """,
            id="doc_limit_offset",
        ),
        pytest.param(
            """
            (
                SELECT 'apples' AS item, 2 AS sales
                UNION ALL
                SELECT 'bananas' AS item, 5 AS sales
                UNION ALL
                SELECT 'carrots' AS item, 8 AS sales
            )
            |> AGGREGATE COUNT(*) AS num_items, SUM(sales) AS total_sales;
            """,
            id="doc_agg",
        ),
        pytest.param(
            """
            (
                SELECT 'apples' AS item, 2 AS sales
                UNION ALL
                SELECT 'bananas' AS item, 5 AS sales
                UNION ALL
                SELECT 'carrots' AS item, 8 AS sales
            )
            |> AGGREGATE COUNT(*) AS num_items, SUM(sales) AS total_sales
               GROUP BY item;
            """,
            id="doc_agg_group_by",
        ),
        pytest.param(
            """
            FROM Produce
            |> AGGREGATE SUM(sales) AS total_sales
               GROUP AND ORDER BY category, item DESC;
            """,
            id="doc_agg_group_and_order_by",
        ),
        pytest.param(
            """
            FROM Produce
            |> AGGREGATE SUM(sales) AS total_sales
               GROUP BY category, item
            |> ORDER BY category, item DESC;
            """,
            id="doc_agg_group_then_order_by",
        ),
        pytest.param(
            """
            FROM Produce
            |> AGGREGATE SUM(sales) AS total_sales ASC
               GROUP BY item, category DESC;
            """,
            id="doc_agg_group_implicit_order_by",
        ),
        pytest.param(
            """
            (
                SELECT 1 AS x
                UNION ALL
                SELECT 3 AS x
                UNION ALL
                SELECT 2 AS x
            )
            |> ORDER BY x DESC;
            """,
            id="doc_order_by",
        ),
        pytest.param(
            """
            SELECT * FROM UNNEST(ARRAY<INT64>[1, 2, 3]) AS number
            |> UNION ALL (SELECT 1);
            """,
            id="doc_union_all",
        ),
        pytest.param(
            """
            SELECT * FROM UNNEST(ARRAY<INT64>[1, 2, 3]) AS number
            |> UNION DISTINCT (SELECT 1);
            """,
            id="doc_union_distinct_single",
        ),
        pytest.param(
            """
            SELECT * FROM UNNEST(ARRAY<INT64>[1, 2, 3]) AS number
            |> UNION DISTINCT
                (SELECT 1),
                (SELECT 2);
            """,
            id="doc_union_distinct_multi",
        ),
        pytest.param(
            """
            SELECT 1 AS one_digit, 10 AS two_digit
            |> UNION ALL BY NAME
                (SELECT 20 AS two_digit, 2 AS one_digit);
            """,
            id="doc_union_all_by_name",
        ),
        pytest.param(
            """
            SELECT 1 AS one_digit, 10 AS two_digit
            |> UNION ALL
                (SELECT 20 AS two_digit, 2 AS one_digit);
            """,
            id="doc_union_all_not_by_name",
        ),
        pytest.param(
            """
            (
                SELECT 1 AS one_digit, 10 AS two_digit
                UNION ALL
                SELECT 2, 20
                UNION ALL
                SELECT 3, 30
            )
            |> INTERSECT DISTINCT BY NAME
                (SELECT 10 AS two_digit, 1 AS one_digit);
            """,
            id="doc_intersect_distinct",
        ),
        pytest.param(
            """
            SELECT * FROM UNNEST(ARRAY<INT64>[1, 2, 3, 3, 4]) AS number
            |> EXCEPT DISTINCT
            (
              SELECT * FROM UNNEST(ARRAY<INT64>[1, 2]) AS number
              |> EXCEPT DISTINCT
                  (SELECT * FROM UNNEST(ARRAY<INT64>[1, 4]) AS number)
            );
            """,
            id="doc_except_distinct_subquery",
        ),
        pytest.param(
            """
            (
                SELECT 'apples' AS item, 2 AS sales
                UNION ALL
                SELECT 'bananas' AS item, 5 AS sales
            )
            |> AS produce_sales
            |> LEFT JOIN
                 (
                   SELECT "apples" AS item, 123 AS id
                 ) AS produce_data
               ON produce_sales.item = produce_data.item
            |> SELECT produce_sales.item, sales, id;
            """,
            id="doc_join",
        ),
        pytest.param(
            """
            FROM input_table
            |> CALL tvf1(arg1)
            |> CALL tvf2(arg2, arg3);
            """,
            id="doc_call",
        ),
        pytest.param(
            """
            FROM LargeTable
            |> TABLESAMPLE SYSTEM (1 PERCENT);
            """,
            id="doc_tablesample",
        ),
        pytest.param(
            """
            (
              SELECT "kale" AS product, 51 AS sales, "Q1" AS quarter
              UNION ALL
              SELECT "kale" AS product, 4 AS sales, "Q1" AS quarter
              UNION ALL
              SELECT "kale" AS product, 45 AS sales, "Q2" AS quarter
              UNION ALL
              SELECT "apple" AS product, 8 AS sales, "Q1" AS quarter
              UNION ALL
              SELECT "apple" AS product, 10 AS sales, "Q2" AS quarter
            )
            |> PIVOT(SUM(sales) FOR quarter IN ('Q1', 'Q2'));
            """,
            id="doc_pivot",
        ),
        pytest.param(
            """
            (
              SELECT 'kale' as product, 55 AS Q1, 45 AS Q2
              UNION ALL
              SELECT 'apple', 8, 10
            )
            |> UNPIVOT(sales FOR quarter IN (Q1, Q2));
            """,
            id="doc_unpivot",
        ),
    ),
)
def test_doc_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)
