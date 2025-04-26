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
    @v_args(inline=True)
    def query_expr(self, query_start, *pipe_exprs):
        return ast.Query(query_start, pipe_exprs if pipe_exprs else None)

    @v_args(inline=True)
    def select(self, select_metadata: Tree, select_list, from_clause=None):
        select_as = next(select_metadata.find_data("select_shape"), None)

        if select_as is None:
            cls = ast.Select
        else:
            select_as = str(select_as).upper()
            if select_as == "STRUCT":
                cls = ast.SelectAsStruct
            elif select_as == "VALUE":
                cls = ast.SelectAsValue
            else:
                raise ValueError("Unexpected select_as: ", select_as)

        all_or_distinct = next(select_metadata.find_data("select_mode"), "ALL")
        all_or_distinct = str(all_or_distinct).upper()
        distinct = all_or_distinct == "DISTINCT"

        return cls(select_list, from_clause, distinct=distinct)

    def select_list(self, select_columns):
        return ast.SelectList(select_columns)

    @v_args(inline=True)
    def select_expr(self, expr, alias=None):
        return ast.SelectColumn(expr, alias)

    @v_args(inline=True)
    def as_alias(self, ident):
        return ast.Alias(ident)

    @v_args(inline=True)
    def ident(self, value):
        return ast.Ident(str(value))

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
        return ast.ArrayLiteral(elements or [])

    def array_literal_item_list(self, elements):
        return [ast.ArrayLiteralElement(element) for element in elements]

    def struct_literal(self, elements):
        elements = [ast.StructLiteralElement(element) for element in elements]
        return ast.StructLiteral(elements)

    @v_args(inline=True)
    def named_struct_literal(self, prefix, elements):
        return ast.StructLiteral(elements)

    def named_struct_literal_item_list(self, elements):
        return elements

    @v_args(inline=True)
    def named_struct_literal_item(self, expr, alias=None):
        return ast.StructLiteralElement(expr, alias)
