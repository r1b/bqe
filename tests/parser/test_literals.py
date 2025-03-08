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

# TODO: xfail
# pytest.param('SELECT """We say: "hello""""', id="literal_string_tdquot_nonempty"),

@pytest.mark.parametrize("sql", (
        pytest.param('SELECT 1', id="literal_integer_decimal"),
        pytest.param('SELECT +1', id="literal_integer_decimal_plus"),
        pytest.param('SELECT -1', id="literal_integer_decimal_minus"),
        pytest.param('SELECT 0xff', id="literal_integer_hex"),
        pytest.param('SELECT 0XFF', id="literal_integer_hex_cap"),
        pytest.param('SELECT +0xff', id="literal_integer_hex_plus"),
        pytest.param('SELECT -0xff', id="literal_integer_hex_minus"),
))
def test_integer_literal_ok(sql, assert_parse_tree):
    assert_parse_tree(sql)
