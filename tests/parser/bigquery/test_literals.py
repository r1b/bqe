import pytest


@pytest.mark.parametrize("sql", (
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
))
def test_string_literal_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)


@pytest.mark.parametrize("sql", (
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
))
def test_string_literal_error(sql, assert_parse_tree_error):
    assert_parse_tree_error(sql)

@pytest.mark.parametrize("sql", (
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
))
def test_bytes_literal_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)


@pytest.mark.parametrize("sql", (
        pytest.param('SELECT b"bytes', id="literal_bytes_dquot_unclosed"),
        pytest.param("SELECT b'bytes", id="literal_bytes_squot_unclosed"),
        pytest.param('SELECT b"""bytes', id="literal_bytes_tdquot_unclosed"),
        pytest.param("SELECT b'''bytes", id="literal_bytes_tsquot_unclosed"),
        pytest.param('SELECT br"bytes', id="literal_bytes_dquot_raw_unclosed"),
        pytest.param("SELECT br'bytes", id="literal_bytes_squot_raw_unclosed"),
        pytest.param('SELECT br"""bytes', id="literal_bytes_tdquot_raw_unclosed"),
        pytest.param("SELECT br'''bytes", id="literal_bytes_tsquot_raw_unclosed"),
        pytest.param('SELECT b"""We say: "hello""""', id="literal_bytes_tdquot_trailing_quot"),
))
def test_bytes_literal_error(sql, assert_parse_tree_error):
    assert_parse_tree_error(sql)


@pytest.mark.parametrize("sql", (
    pytest.param('SELECT 1', id="literal_integer_decimal"),
    pytest.param('SELECT +1', id="literal_integer_decimal_plus"),
    pytest.param('SELECT -1', id="literal_integer_decimal_minus"),
    pytest.param('SELECT 0xff', id="literal_integer_hex"),
    pytest.param('SELECT 0XFF', id="literal_integer_hex_cap"),
    pytest.param('SELECT +0xff', id="literal_integer_hex_plus"),
    pytest.param('SELECT -0xff', id="literal_integer_hex_minus"),
    pytest.param('SELECT 1`alias`', id="literal_integer_quoted_alias_adjacent"),
))
def test_integer_literal_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)


@pytest.mark.parametrize("sql", (
    pytest.param('SELECT 42"foo"', id="literal_integer_string_adjacent"),
    # ref: https://github.com/google/zetasql/blob/a516c6b26d183efc4f56293256bba92e243b7a61/zetasql/parser/lookahead_transformer.h#L327-L330
    # ref: https://github.com/google/zetasql/blob/a516c6b26d183efc4f56293256bba92e243b7a61/zetasql/parser/lookahead_transformer.cc#L1323-L1344
    # To do this in lark, look at `postlex`
    # We're specifically looking for:
    # [..., INTEGER_LITERAL, UNQUOTED_IDENT, ...]
    # where INTEGER_LITERAL end position = UNQUOTED_IDENT start position (no space in between)
    pytest.param("SELECT 1alias", id="literal_integer_ambiguous_alias", marks=pytest.mark.xfail),
))
def test_integer_literal_error(sql, assert_parse_tree_error):
    assert_parse_tree_error(sql)


@pytest.mark.parametrize("sql", (
    pytest.param("SELECT NUMERIC '42'", id="literal_numeric"),
))
def test_numeric_literal_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)

@pytest.mark.parametrize("sql", (
        pytest.param("SELECT BIGNUMERIC '42'", id="literal_bignumeric"),
))
def test_bignumeric_literal_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)

@pytest.mark.parametrize("sql", (
    pytest.param('SELECT 123.456e-67', id="literal_float_dig_dot_dig_lowere_minus_dig"),
    pytest.param('SELECT .1E4', id="literal_float_dot_dig_cape_dig"),
    pytest.param('SELECT 58.', id="literal_float_dig_dot"),
    pytest.param('SELECT 4e2', id="literal_float_dig_lowere_dig"),
))
def test_float_literal_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)


@pytest.mark.parametrize("sql", (
    pytest.param('SELECT (1,2)', id="literal_struct"),
    pytest.param('SELECT (1,2,3)', id="literal_struct_multi"),
))
def test_struct_literal_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)
