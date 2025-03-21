import pytest


@pytest.mark.parametrize("sql", (
    pytest.param("SELECT column1.column2", id="dotted_column_expr_single"),
    pytest.param("SELECT column1.column2.column3", id="dotted_column_expr_multi"),
    pytest.param("SELECT column1 FROM dataset1.table1", id="dotted_table_expr_single"),
    pytest.param("SELECT column1 FROM `project1`.dataset1.table1", id="dotted_table_expr_multi"),
))
def test_dotted_expr_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)


@pytest.mark.parametrize("sql", (
    pytest.param("SELECT column1[0]", id="subscript_expr_integer_literal_single"),
    pytest.param("SELECT column1[0][1]", id="subscript_expr_integer_literal_multi"),
    pytest.param("SELECT column1.column2[0][1]", id="subscript_expr_path_expr_nested"),
    pytest.param("SELECT column1[OFFSET(2)]", id="subscript_expr_offset"),
    pytest.param("SELECT column1['key1']", id="subscript_expr_string_literal"),
))
def test_subscript_expr_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)


@pytest.mark.parametrize("sql", (
    pytest.param("SELECT FUNC()", id="fcall_pos_arg_none"),
    pytest.param("SELECT FUNC(1)", id="fcall_pos_arg_single"),
    pytest.param("SELECT FUNC(1, 2)", id="fcall_pos_arg_multi"),
    pytest.param("SELECT FUNC(name1 => 1)", id="fcall_named_arg_single"),
    pytest.param("SELECT FUNC(name1 => 1, name2 => 2)", id="fcall_named_arg_multi"),
    pytest.param("SELECT FUNC(1, name2 => 2)", id="fcall_kitchen_sink"),
    pytest.param("SELECT NET.IPV4_FROM_INT64(42)", id="fcall_path_expr"),
))
def test_function_call_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)


@pytest.mark.parametrize("sql", (
    pytest.param("SELECT FUNC(", id="fcall_unclosed_paren"),
    pytest.param("SELECT FUNC(,)", id="fcall_comma_only"),
    pytest.param("SELECT FUNC(,1)", id="fcall_pos_comma_leading"),
    pytest.param("SELECT FUNC(1,)", id="fcall_pos_comma_trailing"),
    pytest.param("SELECT FUNC(,name1 => 1)", id="fcall_named_comma_leading"),
    pytest.param("SELECT FUNC(name1 => 1,)", id="fcall_named_comma_trailing"),
    # TODO: Explicit error for this one
    pytest.param("SELECT FUNC(name1 => 1, 2)", id="fcall_named_before_pos"),
))
def test_function_call_error(sql, assert_parse_tree_error):
    assert_parse_tree_error(sql)


@pytest.mark.parametrize("sql", (
    pytest.param("SELECT FUNC(DISTINCT col1)", id="agg_fcall_distinct"),
    pytest.param("SELECT FUNC(col1 IGNORE NULLS)", id="agg_fcall_ignore_nulls"),
    pytest.param("SELECT FUNC(col1 RESPECT NULLS)", id="agg_fcall_respect_nulls"),
    pytest.param("SELECT FUNC(col1 HAVING MIN col2)", id="agg_fcall_having_min"),
    pytest.param("SELECT FUNC(col1 HAVING MAX col2)", id="agg_fcall_having_max"),
    pytest.param("SELECT FUNC(col1 ORDER BY col2 DESC)", id="agg_fcall_order_by"),
    pytest.param("SELECT FUNC(col1 LIMIT 1)", id="agg_fcall_limit"),
))
def test_aggregate_function_call_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)


@pytest.mark.parametrize("sql", (
    pytest.param("SELECT x OR y AND NOT z", id="expr_and_or_not"),
    pytest.param("SELECT (x OR y) AND NOT z", id="expr_and_or_not_parens"),
))
def test_and_or_not_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)


@pytest.mark.parametrize("sql", (
    pytest.param("SELECT x BETWEEN a AND b AND c", id="expr_between"),
))
def test_between(sql, assert_parse_tree):
    assert_parse_tree(sql)
