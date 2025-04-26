import pytest


@pytest.mark.parametrize(
    "sql",
    (
        pytest.param('SELECT ""', id="literal_string_dquot_empty"),
        pytest.param('SELECT "string"', id="literal_string_dquot_nonempty"),
        pytest.param("SELECT ''", id="literal_string_squot_empty"),
        pytest.param("SELECT 'string'", id="literal_string_squot_nonempty"),
        pytest.param('SELECT """"""', id="literal_string_tdquot_empty"),
        pytest.param('SELECT """We say: "hello"."""', id="literal_string_tdquot_nonempty"),
        pytest.param("SELECT ''''''", id="literal_string_tsquot_empty"),
        pytest.param("SELECT '''We say: 'hello'.'''", id="literal_string_tsquot_nonempty"),
        pytest.param('SELECT r""', id="literal_string_dquot_raw_empty"),
        pytest.param('SELECT r"string"', id="literal_string_dquot_raw_nonempty"),
        pytest.param('SELECT R"string"', id="literal_string_dquot_raw_cap"),
        pytest.param("SELECT r''", id="literal_string_squot_raw_empty"),
        pytest.param("SELECT r'string'", id="literal_string_squot_raw_nonempty"),
        pytest.param('SELECT r""""""', id="literal_string_tdquot_raw_empty"),
        pytest.param('SELECT r"""We say: "hello"."""', id="literal_string_tdquot_raw_nonempty"),
        pytest.param("SELECT r''''''", id="literal_string_tsquot_raw_empty"),
        pytest.param("SELECT r'''We say: 'hello'.'''", id="literal_string_tsquot_raw_nonempty"),
    ),
)
def test_string_literal_ok(sql, assert_parse_tree):
    assert_parse_tree(sql, with_ast=True)


@pytest.mark.parametrize(
    "sql",
    (
        pytest.param('SELECT "string', id="literal_string_dquot_unclosed"),
        pytest.param('SELECT string"', id="literal_string_dquot_unopened"),
        pytest.param("SELECT 'string", id="literal_string_squot_unclosed"),
        pytest.param("SELECT string'", id="literal_string_squot_unopened"),
        pytest.param('SELECT """string', id="literal_string_tdquot_unclosed"),
        pytest.param('SELECT string"""', id="literal_string_tdquot_unopened"),
        pytest.param("SELECT '''string", id="literal_string_tsquot_unclosed"),
        pytest.param("SELECT string'''", id="literal_string_tsquot_unopened"),
        pytest.param('SELECT r"string', id="literal_string_dquot_raw_unclosed"),
        pytest.param("SELECT r'string", id="literal_string_squot_raw_unclosed"),
        pytest.param('SELECT r"""string', id="literal_string_tdquot_raw_unclosed"),
        pytest.param("SELECT r'''string", id="literal_string_tsquot_raw_unclosed"),
        pytest.param('SELECT """We say: "hello""""', id="literal_string_tdquot_trailing_quot"),
    ),
)
def test_string_literal_error(sql, assert_parse_tree_error):
    assert_parse_tree_error(sql)


@pytest.mark.parametrize(
    "sql",
    (
        pytest.param('SELECT b""', id="literal_bytes_dquot_empty"),
        pytest.param('SELECT b"bytes"', id="literal_bytes_dquot_nonempty"),
        pytest.param("SELECT b''", id="literal_bytes_squot_empty"),
        pytest.param("SELECT b'bytes'", id="literal_bytes_squot_nonempty"),
        pytest.param('SELECT b""""""', id="literal_bytes_tdquot_empty"),
        pytest.param('SELECT b"""We say: "hello"."""', id="literal_bytes_tdquot_nonempty"),
        pytest.param("SELECT b''''''", id="literal_bytes_tsquot_empty"),
        pytest.param("SELECT b'''We say: 'hello'.'''", id="literal_bytes_tsquot_nonempty"),
        pytest.param('SELECT br""', id="literal_bytes_dquot_raw_empty"),
        pytest.param('SELECT rb"bytes"', id="literal_bytes_dquot_raw_nonempty"),
        pytest.param('SELECT BR"bytes"', id="literal_bytes_dquot_raw_cap"),
        pytest.param("SELECT br''", id="literal_bytes_squot_raw_empty"),
        pytest.param("SELECT br'bytes'", id="literal_bytes_squot_raw_nonempty"),
        pytest.param('SELECT br""""""', id="literal_bytes_tdquot_raw_empty"),
        pytest.param('SELECT br"""We say: "hello"."""', id="literal_bytes_tdquot_raw_nonempty"),
        pytest.param("SELECT br''''''", id="literal_bytes_tsquot_raw_empty"),
        pytest.param("SELECT br'''We say: 'hello'.'''", id="literal_bytes_tsquot_raw_nonempty"),
    ),
)
def test_bytes_literal_ok(sql, assert_parse_tree):
    assert_parse_tree(sql, with_ast=True)


@pytest.mark.parametrize(
    "sql",
    (
        pytest.param('SELECT b"bytes', id="literal_bytes_dquot_unclosed"),
        pytest.param("SELECT b'bytes", id="literal_bytes_squot_unclosed"),
        pytest.param('SELECT b"""bytes', id="literal_bytes_tdquot_unclosed"),
        pytest.param("SELECT b'''bytes", id="literal_bytes_tsquot_unclosed"),
        pytest.param('SELECT br"bytes', id="literal_bytes_dquot_raw_unclosed"),
        pytest.param("SELECT br'bytes", id="literal_bytes_squot_raw_unclosed"),
        pytest.param('SELECT br"""bytes', id="literal_bytes_tdquot_raw_unclosed"),
        pytest.param("SELECT br'''bytes", id="literal_bytes_tsquot_raw_unclosed"),
        pytest.param('SELECT b"""We say: "hello""""', id="literal_bytes_tdquot_trailing_quot"),
    ),
)
def test_bytes_literal_error(sql, assert_parse_tree_error):
    assert_parse_tree_error(sql)


@pytest.mark.parametrize(
    "sql",
    (
        pytest.param("SELECT 1", id="literal_integer_decimal"),
        pytest.param("SELECT 0xff", id="literal_integer_hex"),
        pytest.param("SELECT 0XFF", id="literal_integer_hex_cap"),
        pytest.param("SELECT 1`alias`", id="literal_integer_quoted_alias_adjacent"),
    ),
)
def test_integer_literal_ok(sql, assert_parse_tree):
    assert_parse_tree(sql, with_ast=True)


@pytest.mark.parametrize(
    "sql",
    (
        pytest.param('SELECT 42"foo"', id="literal_integer_string_adjacent"),
        pytest.param(
            "SELECT 1alias", id="literal_integer_ambiguous_alias", marks=pytest.mark.xfail
        ),
    ),
)
def test_integer_literal_error(sql, assert_parse_tree_error):
    assert_parse_tree_error(sql)


@pytest.mark.parametrize("sql", (pytest.param("SELECT NUMERIC '42'", id="literal_numeric"),))
def test_numeric_literal_ok(sql, assert_parse_tree):
    assert_parse_tree(sql, with_ast=True)


@pytest.mark.parametrize("sql", (pytest.param("SELECT BIGNUMERIC '42'", id="literal_bignumeric"),))
def test_bignumeric_literal_ok(sql, assert_parse_tree):
    assert_parse_tree(sql, with_ast=True)


@pytest.mark.parametrize(
    "sql",
    (
        pytest.param("SELECT 123.456e-67", id="literal_float_dig_dot_dig_lower_e_minus_dig"),
        pytest.param("SELECT .1E4", id="literal_float_dot_dig_cap_e_dig"),
        pytest.param("SELECT 58.", id="literal_float_dig_dot"),
        pytest.param("SELECT 4e2", id="literal_float_dig_lower_e_dig"),
    ),
)
def test_float_literal_ok(sql, assert_parse_tree):
    assert_parse_tree(sql, with_ast=True)


@pytest.mark.parametrize(
    "sql",
    (
        pytest.param("SELECT []", id="literal_array_empty"),
        pytest.param("SELECT [1]", id="literal_array_single"),
        pytest.param("SELECT [1,2,3]", id="literal_array_multi"),
        pytest.param("SELECT ARRAY [1,2,3]", id="literal_array_prefix"),
        pytest.param("SELECT ARRAY<INT64>[1,2,3]", id="literal_array_prefix_scalar_type"),
        pytest.param(
            "SELECT ARRAY<STRUCT<a INT64>>[STRUCT(1)]", id="literal_array_prefix_compound_type"
        ),
        pytest.param(
            "SELECT ARRAY<STRUCT<a STRUCT<b INT64>>>[STRUCT(STRUCT(1))]",
            id="literal_array_prefix_nested_compound_type",
        ),
    ),
)
def test_array_literal_ok(sql, assert_parse_tree):
    assert_parse_tree(sql, with_ast=True)


@pytest.mark.parametrize(
    "sql",
    (
        pytest.param("SELECT DATE '1970-01-01'", id="literal_date"),
        pytest.param("SELECT DATE '12:00:00.01'", id="literal_time"),
        pytest.param("SELECT DATETIME '1970-01-01 12:00:00.01'", id="literal_datetime"),
        pytest.param("SELECT TIMESTAMP '1970-01-01 12:00:00.01-08'", id="literal_timestamp"),
    ),
)
def test_date_time_literal_ok(sql, assert_parse_tree):
    assert_parse_tree(sql, with_ast=True)


@pytest.mark.parametrize(
    "sql",
    (
        pytest.param("SELECT RANGE<DATE> '[1970-01-01, 1970-01-02)'", id="literal_range_date"),
        pytest.param(
            "SELECT RANGE<DATETIME> '[1970-01-01 00:00:00, 1970-01-02 00:00:00)'",
            id="literal_range_datetime",
        ),
        pytest.param(
            "SELECT RANGE<TIMESTAMP> '[1970-01-01 00:00:00.45-08, 1970-01-02 00:00:00.45-08)'",
            id="literal_range_timestamp",
        ),
    ),
)
def test_range_literal_ok(sql, assert_parse_tree):
    assert_parse_tree(sql, with_ast=True)


@pytest.mark.parametrize("sql", (pytest.param("SELECT JSON '{}'", id="literal_json"),))
def test_json_literal_ok(sql, assert_parse_tree):
    assert_parse_tree(sql, with_ast=True)


@pytest.mark.parametrize(
    "sql",
    (
        pytest.param("SELECT (1, 2)", id="literal_struct"),
        pytest.param("SELECT (1, 2, 3)", id="literal_struct_multi"),
        pytest.param("SELECT STRUCT(1, 2, 3)", id="literal_struct_named"),
        pytest.param("SELECT STRUCT(1 AS a, 2 AS b, 3 AS c)", id="literal_struct_named_alias"),
        pytest.param(
            "SELECT STRUCT<INT64, INT64, INT64>(1, 2, 3)",
            id="literal_struct_named_compound_type_decl",
        ),
        pytest.param(
            "SELECT STRUCT<a INT64, b INT64, c INT64>(1, 2, 3)",
            id="literal_struct_named_compound_type_decl_column",
        ),
        pytest.param(
            "SELECT STRUCT<a INT64, STRUCT<b INT64, c INT64>>(1, STRUCT(2, 3))",
            id="literal_struct_named_compound_type_decl_nested",
        ),
    ),
)
def test_struct_literal_ok(sql, assert_parse_tree):
    assert_parse_tree(sql, with_ast=True)


@pytest.mark.parametrize(
    "sql",
    (
        pytest.param("SELECT tRue", id="literal_boolean_true"),
        pytest.param("SELECT False", id="literal_boolean_false"),
    ),
)
def test_boolean_literal_ok(sql, assert_parse_tree):
    assert_parse_tree(sql, with_ast=True)


@pytest.mark.parametrize(
    "sql",
    (pytest.param("SELECT null", id="literal_null"),),
)
def test_null_literal_ok(sql, assert_parse_tree):
    assert_parse_tree(sql, with_ast=True)
