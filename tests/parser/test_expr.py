import pytest


@pytest.mark.parametrize(
    "sql",
    (
        pytest.param("SELECT column1.column2", id="dotted_column_expr_single"),
        pytest.param("SELECT column1.column2.column3", id="dotted_column_expr_multi"),
        pytest.param("SELECT column1 FROM dataset1.table1", id="dotted_table_expr_single"),
        pytest.param(
            "SELECT column1 FROM `project1`.dataset1.table1", id="dotted_table_expr_multi"
        ),
    ),
)
def test_dotted_expr_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)


@pytest.mark.parametrize(
    "sql",
    (
        pytest.param("SELECT column1[0]", id="subscript_expr_integer_literal_single"),
        pytest.param("SELECT column1[0][1]", id="subscript_expr_integer_literal_multi"),
        pytest.param("SELECT column1.column2[0][1]", id="subscript_expr_path_expr_nested"),
        pytest.param("SELECT column1[OFFSET(2)]", id="subscript_expr_offset"),
        pytest.param("SELECT column1['key1']", id="subscript_expr_string_literal"),
    ),
)
def test_subscript_expr_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)


@pytest.mark.parametrize(
    "sql",
    (
        pytest.param("SELECT FUNC()", id="fcall_pos_arg_none"),
        pytest.param("SELECT FUNC(1)", id="fcall_pos_arg_single"),
        pytest.param("SELECT FUNC(1, 2)", id="fcall_pos_arg_multi"),
        pytest.param("SELECT FUNC(name1 => 1)", id="fcall_named_arg_single"),
        pytest.param("SELECT FUNC(name1 => 1, name2 => 2)", id="fcall_named_arg_multi"),
        pytest.param("SELECT FUNC(1, name2 => 2)", id="fcall_kitchen_sink"),
        pytest.param("SELECT NET.IPV4_FROM_INT64(42)", id="fcall_path_expr"),
        pytest.param("SELECT FUNC(*)", id="fcall_star_expr"),
    ),
)
def test_function_call_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)


@pytest.mark.parametrize(
    "sql",
    (
        pytest.param("SELECT FUNC(", id="fcall_unclosed_paren"),
        pytest.param("SELECT FUNC(,)", id="fcall_comma_only"),
        pytest.param("SELECT FUNC(,1)", id="fcall_pos_comma_leading"),
        pytest.param("SELECT FUNC(1,)", id="fcall_pos_comma_trailing"),
        pytest.param("SELECT FUNC(,name1 => 1)", id="fcall_named_comma_leading"),
        pytest.param("SELECT FUNC(name1 => 1,)", id="fcall_named_comma_trailing"),
        # TODO: Explicit error for this one
        pytest.param("SELECT FUNC(name1 => 1, 2)", id="fcall_named_before_pos"),
    ),
)
def test_function_call_error(sql, assert_parse_tree_error):
    assert_parse_tree_error(sql)


@pytest.mark.parametrize(
    "sql",
    (
        pytest.param("SELECT FUNC(DISTINCT col1)", id="agg_fcall_distinct"),
        pytest.param("SELECT FUNC(col1 IGNORE NULLS)", id="agg_fcall_ignore_nulls"),
        pytest.param("SELECT FUNC(col1 RESPECT NULLS)", id="agg_fcall_respect_nulls"),
        pytest.param("SELECT FUNC(col1 HAVING MIN col2)", id="agg_fcall_having_min"),
        pytest.param("SELECT FUNC(col1 HAVING MAX col2)", id="agg_fcall_having_max"),
        pytest.param("SELECT FUNC(col1 ORDER BY col2 DESC)", id="agg_fcall_order_by"),
        pytest.param("SELECT FUNC(col1 LIMIT 1)", id="agg_fcall_limit"),
    ),
)
def test_aggregate_function_call_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)


@pytest.mark.parametrize(
    "sql",
    (
        pytest.param("SELECT x OR y", id="expr_or"),
        pytest.param("SELECT x AND y", id="expr_and"),
        pytest.param("SELECT (x OR y) OR z", id="expr_parens"),
        pytest.param("SELECT NOT x", id="expr_not"),
        pytest.param("SELECT x IS DISTINCT FROM y", id="expr_is_distinct_from"),
        pytest.param("SELECT x IS TRUE", id="expr_is"),
        pytest.param("SELECT x IS NOT NULL", id="expr_is_not"),
        pytest.param("SELECT x NOT IN UNNEST([1,2,3])", id="expr_not_in"),
        pytest.param("SELECT x IN (1,2,3)", id="expr_in"),
        pytest.param("SELECT x NOT BETWEEN y AND z", id="expr_not_between"),
        pytest.param("SELECT x BETWEEN y AND z", id="expr_between"),
        pytest.param("SELECT x NOT LIKE ALL ('a%','%b')", id="expr_not_qlike"),
        pytest.param("SELECT x LIKE ANY UNNEST(['a%','%b'])", id="expr_qlike"),
        pytest.param("SELECT x NOT LIKE 'a%'", id="expr_not_like"),
        pytest.param("SELECT x LIKE 'a%'", id="expr_like"),
        pytest.param("SELECT x != y", id="expr_ne"),
        pytest.param("SELECT x <> y", id="expr_ne_var"),
        pytest.param("SELECT x >= y", id="expr_gte"),
        pytest.param("SELECT x <= y", id="expr_lte"),
        pytest.param("SELECT x > y", id="expr_gt"),
        pytest.param("SELECT x < y", id="expr_lt"),
        pytest.param("SELECT x = y", id="expr_eq"),
        pytest.param("SELECT x | y", id="expr_bitwise_or"),
        pytest.param("SELECT x ^ y", id="expr_bitwise_xor"),
        pytest.param("SELECT x & y", id="expr_bitwise_and"),
        pytest.param("SELECT x >> y", id="expr_bitwise_shr"),
        pytest.param("SELECT x - y", id="expr_sub"),
        pytest.param("SELECT x + y", id="expr_add"),
        pytest.param("SELECT x / y", id="expr_div"),
        pytest.param("SELECT x * y", id="expr_mul"),
        pytest.param("SELECT ~x", id="expr_bitwise_not"),
        pytest.param("SELECT -x", id="expr_uminus"),
        pytest.param("SELECT +x", id="expr_uplus"),
        pytest.param("SELECT x[0]", id="expr_subscript"),
        pytest.param("SELECT x.y", id="expr_field_access"),
    ),
)
def test_column_expr_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)


@pytest.mark.parametrize(
    "sql",
    (
        pytest.param("SELECT x OR y AND NOT z", id="expr_and_or_not"),
        pytest.param("SELECT (x OR y) AND NOT z", id="expr_and_or_not_parens"),
    ),
)
def test_and_or_not_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)


@pytest.mark.parametrize(
    "sql", (pytest.param("SELECT x BETWEEN a AND b AND c", id="expr_between"),)
)
def test_between_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)


@pytest.mark.parametrize(
    "sql",
    (
        pytest.param("SELECT ARRAY(SELECT 1)", id="keyword_subquery_array"),
        pytest.param("SELECT EXISTS(SELECT 1)", id="keyword_subquery_exists"),
    ),
)
def test_keyword_subquery_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)


@pytest.mark.parametrize(
    "sql",
    (
        pytest.param("SELECT CASE WHEN 1 THEN 1 END", id="case_single"),
        pytest.param("SELECT CASE WHEN 1 THEN 1 WHEN 2 THEN 2 END", id="case_multi"),
        pytest.param("SELECT CASE WHEN 1 THEN 1 WHEN 2 THEN 2 ELSE 3 END", id="case_multi_else"),
        pytest.param("SELECT CASE col1 WHEN 1 THEN 1 END", id="case_match_single"),
        pytest.param("SELECT CASE col1 WHEN 1 THEN 1 WHEN 2 THEN 2 END", id="case_match_multi"),
        pytest.param(
            "SELECT CASE col1 WHEN 1 THEN 1 WHEN 2 THEN 2 ELSE 3 END", id="case_match_multi_else"
        ),
    ),
)
def test_case_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)
