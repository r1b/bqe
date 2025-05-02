from lark import Token, Transformer, Tree, v_args
from lark.tree import Meta
from bqe import ast


def fuse_meta(m1: Meta, m2: Meta) -> Meta:
    """Reconstruct metadata for transformed trees.
    ASSUMPTION: m1 is the immediate parent of m2.
    TODO: Include the rest of the metadata
    """
    new_meta = Meta()
    new_meta.empty = False
    new_meta.start_pos = m1.start_pos
    new_meta.end_pos = m2.end_pos
    return new_meta


class ParserTransformer(Transformer):
    """First-pass transformer. Use this to clean up stuff that is meaningless after parsing.
    Operates on `lark.Tree`."""

    @v_args(meta=True)
    def ident(self, meta, args):
        """Rewrite keyword_as_ident to ident"""
        child = args[0]
        if isinstance(child, Tree) and child.data == "keyword_as_ident":
            return Tree("ident", child.children, meta)
        return Tree("ident", args, meta)

    @v_args(meta=True)
    def field_access_expr(self, meta, args):
        """Rewrite left-recursive field_access_expr to path_expression.
        When a non-ident lhs is encountered, rewrite to dot_ident."""
        parent, child = args
        if parent.data == "ident":
            return Tree("path_expression", args, meta)
        if parent.data in ("field_access_expr", "path_expression"):
            lhs, rhs = parent.children, [child]
            children = lhs + rhs
            return Tree("path_expression", children, fuse_meta(meta, child.meta))
        return Tree("dot_ident", args, meta)

    @v_args(meta=True)
    def subquery(self, meta, args):
        """Collapse nested subqueries. TODO: This doesn't belong here"""
        child = args[0]
        if child.data == "subquery":
            return Tree("subquery", child.children, fuse_meta(meta, child.meta))
        return Tree("subquery", args, meta)


class AstTransformer(Transformer):
    """Second-pass transformer. Use this to construct an AST.
    Operates on `ast.Node`."""

    # Queries

    @v_args(meta=True, inline=True)
    def query_expr(self, meta, query_start, *pipe_exprs):
        return ast.Query(query_start, pipe_exprs if pipe_exprs else None).with_metadata(meta)

    @v_args(meta=True, inline=True)
    def subquery(self, meta, query_expr):
        return ast.Subquery(query_expr).with_metadata(meta)

    # SELECT

    @v_args(meta=True, inline=True)
    def select(self, meta, select_as, select_list, from_clause):
        if select_as is None:
            cls = ast.Select
        else:
            if select_as == "STRUCT":
                cls = ast.SelectAsStruct
            elif select_as == "VALUE":
                cls = ast.SelectAsValue
            else:
                raise ValueError("Unexpected select_as: ", select_as)

        return cls(select_list, from_clause).with_metadata(meta)

    @v_args(inline=True)
    def select_shape(self, select_as):
        return str(select_as).upper()

    @v_args(meta=True)
    def select_list(self, meta, select_columns):
        return ast.SelectList(select_columns).with_metadata(meta)

    @v_args(meta=True, inline=True)
    def select_expr(self, meta, expr, alias=None):
        return ast.SelectColumn(expr, alias).with_metadata(meta)

    @v_args(meta=True, inline=True)
    def select_star(self, meta, except_modifiers, replace_modifiers):
        return ast.SelectStar(except_modifiers, replace_modifiers).with_metadata(meta)

    @v_args(meta=True, inline=True)
    def select_dot_star(self, meta, path, except_modifiers, replace_modifiers):
        return ast.SelectDotStar(path, except_modifiers, replace_modifiers).with_metadata(meta)

    @v_args(inline=True)
    def select_except(self, except_modifiers):
        return except_modifiers

    @v_args(meta=True)
    def select_except_list(self, meta, except_items):
        return ast.ExceptModifierList(except_items).with_metadata(meta)

    @v_args(meta=True, inline=True)
    def select_except_item(self, meta, ident):
        return ast.ExceptModifierItem(ident).with_metadata(meta)

    @v_args(inline=True)
    def select_replace(self, replace_modifiers):
        return replace_modifiers

    @v_args(meta=True)
    def select_replace_list(self, meta, replace_items):
        return ast.ReplaceModifierList(replace_items).with_metadata(meta)

    @v_args(meta=True, inline=True)
    def select_replace_item(self, meta, expr, alias):
        return ast.ReplaceModifierItem(expr, alias).with_metadata(meta)

    @v_args(meta=True, inline=True)
    def from_clause(self, meta, expr):
        return ast.FromClause(expr).with_metadata(meta)

    @v_args(meta=True, inline=True)
    def from_item_table(self, meta, path, alias, time_travel):
        return ast.TablePathExpression(path, alias, time_travel).with_metadata(meta)

    @v_args(meta=True, inline=True)
    def time_travel(self, meta, expr):
        return ast.TimeTravel(expr).with_metadata(meta)

    @v_args(meta=True, inline=True)
    def from_item_subquery(self, meta, subquery, alias):
        return ast.TableSubquery(subquery, alias).with_metadata(meta)

    @v_args(meta=True, inline=True)
    def from_item_unnest(self, meta, unnest_expr, alias, with_offset):
        return ast.TableUnnestExpression(unnest_expr, alias, with_offset).with_metadata(meta)

    @v_args(meta=True, inline=True)
    def unnest_expr(self, meta, expr):
        return ast.UnnestExpression(expr).with_metadata(meta)

    @v_args(meta=True, inline=True)
    def from_unnest_offset_expr(self, meta, alias):
        return ast.WithOffset(alias).with_metadata(meta)

    # Names

    @v_args(meta=True, inline=True)
    def as_alias(self, meta, ident):
        return ast.Alias(ident).with_metadata(meta)

    @v_args(meta=True, inline=True)
    def ident(self, meta, value):
        return ast.Ident(str(value)).with_metadata(meta)

    @v_args(meta=True)
    def path_expression(self, meta, components):
        return ast.PathExpression(components).with_metadata(meta)

    # Literals

    @v_args(meta=True, inline=True)
    def integer_literal(self, meta, value):
        return ast.IntegerLiteral(str(value)).with_metadata(meta)

    @v_args(meta=True, inline=True)
    def string_literal(self, meta, value):
        return ast.StringLiteral(str(value)).with_metadata(meta)

    @v_args(meta=True, inline=True)
    def bytes_literal(self, meta, value):
        return ast.BytesLiteral(str(value)).with_metadata(meta)

    @v_args(meta=True, inline=True)
    def numeric_literal(self, meta, value):
        return ast.NumericLiteral(str(value)).with_metadata(meta)

    @v_args(meta=True, inline=True)
    def bignumeric_literal(self, meta, value):
        return ast.BigNumericLiteral(str(value)).with_metadata(meta)

    @v_args(meta=True, inline=True)
    def float_literal(self, meta, value):
        return ast.FloatLiteral(str(value)).with_metadata(meta)

    @v_args(meta=True, inline=True)
    def date_literal(self, meta, value):
        return ast.DateLiteral(str(value)).with_metadata(meta)

    @v_args(meta=True, inline=True)
    def datetime_literal(self, meta, value):
        return ast.DatetimeLiteral(str(value)).with_metadata(meta)

    @v_args(meta=True, inline=True)
    def timestamp_literal(self, meta, value):
        return ast.TimestampLiteral(str(value)).with_metadata(meta)

    @v_args(meta=True, inline=True)
    def range_literal(self, meta, range_type, value):
        if range_type == "DATE":
            cls = ast.DateRangeLiteral
        elif range_type == "DATETIME":
            cls = ast.DatetimeRangeLiteral
        elif range_type == "TIMESTAMP":
            cls = ast.TimestampRangeLiteral
        else:
            raise ValueError("Unexpected range_type: ", range_type)

        return cls(value).with_metadata(meta)

    @v_args(inline=True)
    def range_type(self, type_: Tree):
        # TODO: Hack until we actually care about structured types
        return str(next(type_.scan_values(lambda v: isinstance(v, Token))))

    @v_args(inline=True)
    def range_value(self, value):
        return str(value)

    @v_args(meta=True, inline=True)
    def json_literal(self, meta, value):
        return ast.JsonLiteral(str(value)).with_metadata(meta)

    @v_args(meta=True, inline=True)
    def array_literal(self, meta, prefix, elements=None):
        # TODO: Handle type
        return ast.ArrayLiteral(elements or []).with_metadata(meta)

    def array_literal_item_list(self, elements):
        return elements

    @v_args(meta=True, inline=True)
    def array_literal_item(self, meta, element):
        return ast.ArrayLiteralElement(element).with_metadata(meta)

    @v_args(meta=True)
    def struct_literal(self, meta, elements):
        return ast.StructLiteral(elements).with_metadata(meta)

    @v_args(meta=True, inline=True)
    def struct_literal_item(self, meta, element):
        return ast.StructLiteralElement(element).with_metadata(meta)

    @v_args(meta=True, inline=True)
    def named_struct_literal(self, meta, prefix, elements):
        # TODO: Handle type
        return ast.StructLiteral(elements).with_metadata(meta)

    def named_struct_literal_item_list(self, elements):
        return elements

    @v_args(meta=True, inline=True)
    def named_struct_literal_item(self, meta, expr, alias=None):
        return ast.StructLiteralElement(expr, alias).with_metadata(meta)

    @v_args(meta=True, inline=True)
    def boolean_literal(self, meta, value):
        return ast.BooleanLiteral(str(value).upper()).with_metadata(meta)

    @v_args(meta=True, inline=True)
    def null_literal(self, meta, _):
        return ast.NullLiteral().with_metadata(meta)
