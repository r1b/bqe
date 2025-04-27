from lark import Token, Transformer, Tree, v_args
from bqe import ast


class ParserTransformer(Transformer):
    def ident(self, args):
        """Rewrite keyword_as_ident to ident"""
        child = args[0]
        if isinstance(child, Tree) and child.data == "keyword_as_ident":
            return Tree("ident", child.children)
        return Tree("ident", args)

    def field_access_expr(self, args):
        """Rewrite left-recursive field_access_expr to path_expression.
        When a non-ident lhs is encountered, rewrite to dot_ident."""
        parent, child = args
        if parent.data == "ident":
            return Tree("path_expression", args)
        if parent.data in ("field_access_expr", "path_expression"):
            lhs, rhs = parent.children, [child]
            children = lhs + rhs
            return Tree("path_expression", children)
        return Tree("dot_ident", args)

    def subquery(self, args):
        """Collapse nested subqueries."""
        child = args[0]
        if child.data == "subquery":
            return Tree("subquery", child.children)
        return Tree("subquery", args)


class AstTransformer(Transformer):
    # Queries

    @v_args(inline=True)
    def query_expr(self, query_start, *pipe_exprs):
        return ast.Query(query_start, pipe_exprs if pipe_exprs else None)

    @v_args(inline=True)
    def subquery(self, query_expr):
        return ast.Subquery(query_expr)

    # SELECT

    @v_args(inline=True)
    def select(self, all_or_distinct, select_as, select_list, from_clause):
        if select_as is None:
            cls = ast.Select
        else:
            if select_as == "STRUCT":
                cls = ast.SelectAsStruct
            elif select_as == "VALUE":
                cls = ast.SelectAsValue
            else:
                raise ValueError("Unexpected select_as: ", select_as)

        all_or_distinct = all_or_distinct or "ALL"
        distinct = all_or_distinct == "DISTINCT"

        return cls(select_list, from_clause, distinct=distinct)

    @v_args(inline=True)
    def select_mode(self, all_or_distinct):
        return str(all_or_distinct).upper()

    @v_args(inline=True)
    def select_shape(self, select_as):
        return str(select_as).upper()

    def select_list(self, select_columns):
        return ast.SelectList(select_columns)

    @v_args(inline=True)
    def select_expr(self, expr, alias=None):
        return ast.SelectColumn(expr, alias)

    @v_args(inline=True)
    def select_star(self, except_modifiers, replace_modifiers):
        return ast.SelectStar(except_modifiers, replace_modifiers)

    @v_args(inline=True)
    def select_dot_star(self, path, except_modifiers, replace_modifiers):
        return ast.SelectDotStar(path, except_modifiers, replace_modifiers)

    @v_args(inline=True)
    def select_except(self, except_modifiers):
        return except_modifiers

    def select_except_list(self, except_items):
        return ast.ExceptModifierList(except_items)

    @v_args(inline=True)
    def select_except_item(self, ident):
        return ast.ExceptModifierItem(ident)

    @v_args(inline=True)
    def select_replace(self, replace_modifiers):
        return replace_modifiers

    def select_replace_list(self, replace_items):
        return ast.ReplaceModifierList(replace_items)

    @v_args(inline=True)
    def select_replace_item(self, expr, alias):
        return ast.ReplaceModifierItem(expr, alias)

    @v_args(inline=True)
    def from_clause(self, expr):
        return ast.FromClause(expr)

    @v_args(inline=True)
    def from_item_table(self, path, alias, time_travel):
        return ast.TablePathExpression(path, alias, time_travel)

    @v_args(inline=True)
    def time_travel(self, expr):
        return ast.TimeTravel(expr)

    @v_args(inline=True)
    def from_item_subquery(self, subquery, alias):
        return ast.TableSubquery(subquery, alias)

    @v_args(inline=True)
    def from_item_unnest(self, unnest_expr, alias, with_offset):
        return ast.TableUnnestExpression(unnest_expr, alias, with_offset)

    @v_args(inline=True)
    def unnest_expr(self, expr):
        return ast.UnnestExpression(expr)

    @v_args(inline=True)
    def from_unnest_offset_expr(self, alias):
        return ast.WithOffset(alias)

    # Names

    @v_args(inline=True)
    def as_alias(self, ident):
        return ast.Alias(ident)

    @v_args(inline=True)
    def ident(self, value):
        return ast.Ident(str(value))

    def path_expression(self, components):
        return ast.PathExpression(components)

    # Literals

    @v_args(inline=True)
    def integer_literal(self, value):
        return ast.IntegerLiteral(str(value))

    @v_args(inline=True)
    def string_literal(self, value):
        return ast.StringLiteral(str(value))

    @v_args(inline=True)
    def bytes_literal(self, value):
        return ast.BytesLiteral(str(value))

    @v_args(inline=True)
    def numeric_literal(self, value):
        return ast.NumericLiteral(str(value))

    @v_args(inline=True)
    def bignumeric_literal(self, value):
        return ast.BigNumericLiteral(str(value))

    @v_args(inline=True)
    def float_literal(self, value):
        return ast.FloatLiteral(str(value))

    @v_args(inline=True)
    def date_literal(self, value):
        return ast.DateLiteral(str(value))

    @v_args(inline=True)
    def datetime_literal(self, value):
        return ast.DatetimeLiteral(str(value))

    @v_args(inline=True)
    def timestamp_literal(self, value):
        return ast.TimestampLiteral(str(value))

    @v_args(inline=True)
    def range_literal(self, range_type, value):
        if range_type == "DATE":
            return ast.DateRangeLiteral(value)
        elif range_type == "DATETIME":
            return ast.DatetimeRangeLiteral(value)
        elif range_type == "TIMESTAMP":
            return ast.TimestampRangeLiteral(value)
        else:
            raise ValueError("Unexpected range_type: ", range_type)

    @v_args(inline=True)
    def range_type(self, type_: Tree):
        # TODO: Hack until we actually care about structured types
        return str(next(type_.scan_values(lambda v: isinstance(v, Token))))

    @v_args(inline=True)
    def range_value(self, value):
        return str(value)

    @v_args(inline=True)
    def json_literal(self, value):
        return ast.JsonLiteral(str(value))

    @v_args(inline=True)
    def array_literal(self, prefix, elements=None):
        # TODO: Handle type
        return ast.ArrayLiteral(elements or [])

    def array_literal_item_list(self, elements):
        return [ast.ArrayLiteralElement(element) for element in elements]

    def struct_literal(self, elements):
        elements = [ast.StructLiteralElement(element) for element in elements]
        return ast.StructLiteral(elements)

    @v_args(inline=True)
    def named_struct_literal(self, prefix, elements):
        # TODO: Handle type
        return ast.StructLiteral(elements)

    def named_struct_literal_item_list(self, elements):
        return elements

    @v_args(inline=True)
    def named_struct_literal_item(self, expr, alias=None):
        return ast.StructLiteralElement(expr, alias)

    @v_args(inline=True)
    def boolean_literal(self, value):
        return ast.BooleanLiteral(str(value).upper())

    @v_args(inline=True)
    def null_literal(self, _):
        return ast.NullLiteral()
