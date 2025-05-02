from typing import Optional
from lark.tree import Meta


def pretty(node: "Node", indent="  ", nl="\n", max_snippet_size=32, sql=None):
    """Pretty-print an AST."""

    def render(s: str, depth: int):
        prefix = ""
        if depth > 0:
            prefix += nl
            prefix += depth * indent
        return prefix + s

    def _pretty(node: "Node", depth: int):
        result = render(type(node).__name__, depth)

        args = []

        if node._value:
            value = getattr(node, node._value)
            if value is not None:
                args.append(str(value))

        if node._options:
            for option_name in node._options:
                option = getattr(node, option_name)
                if option is not None:
                    args.append(f"{option_name}={str(option)}")

        if args:
            result += "(" + ", ".join(args) + ")"

        if node._metadata is not None:
            metadata = node._metadata
            result += f" [{metadata.start_pos}-{metadata.end_pos}]"
            if sql is not None:
                snippet = sql[metadata.start_pos : metadata.end_pos]
                snippet = " ".join(snippet.split())
                if len(snippet) > max_snippet_size:
                    snippet_part_size = max_snippet_size // 2
                    snippet = snippet[:snippet_part_size] + "..." + snippet[-snippet_part_size:]

                result += f" {{{snippet}}}"

        for child_name in node._children:
            child = getattr(node, child_name)
            if child is not None:
                if not isinstance(child, list):
                    child = [child]
                for element in child:
                    result += _pretty(element, depth + 1)

        return result

    return _pretty(node, 0)


class Node:
    _children: tuple[str, ...] = ()
    _options: tuple[str, ...] = ()
    _value: Optional[str] = None

    _metadata: Optional[Meta] = None

    def with_metadata(self, metadata: Meta):
        if not metadata.empty:
            self._metadata = metadata
        return self


class Query(Node):
    _children = ("query_expr", "pipe_exprs")

    def __init__(self, query_expr: Node, pipe_exprs: Optional[list[Node]] = None):
        self.query_expr = query_expr
        self.pipe_exprs = pipe_exprs


class Subquery(Node):
    _children = ("query_expr",)

    def __init__(self, query_expr: Node):
        self.query_expr = query_expr


class Select(Node):
    _children = ("select_list", "from_clause")

    def __init__(self, select_list: Node, from_clause: Optional[Node] = None):
        self.select_list = select_list
        self.from_clause = from_clause


class SelectAsStruct(Select):
    pass


class SelectAsValue(Select):
    pass


class SelectList(Node):
    _children = ("select_columns",)

    def __init__(
        self,
        select_columns: list[Node],
    ):
        self.select_columns = select_columns


class SelectColumn(Node):
    _children = ("expr", "alias")

    def __init__(self, expr: Node, alias: Optional[Node] = None):
        self.expr = expr
        self.alias = alias


class SelectStar(Node):
    _children = ("except_modifiers", "replace_modifiers")

    def __init__(
        self, except_modifiers: Optional[Node] = None, replace_modifiers: Optional[Node] = None
    ):
        self.except_modifiers = except_modifiers
        self.replace_modifiers = replace_modifiers


class SelectDotStar(Node):
    _children = ("path", "except_modifiers", "replace_modifiers")

    def __init__(
        self,
        path: Node,
        except_modifiers: Optional[Node] = None,
        replace_modifiers: Optional[Node] = None,
    ):
        self.path = path
        self.except_modifiers = except_modifiers
        self.replace_modifiers = replace_modifiers


class ExceptModifierList(Node):
    _children = ("items",)

    def __init__(self, items: list[Node]):
        self.items = items


class ReplaceModifierList(Node):
    _children = ("items",)

    def __init__(self, items: list[Node]):
        self.items = items


class ExceptModifierItem(Node):
    _children = ("ident",)

    def __init__(self, ident: Node):
        self.ident = ident


class ReplaceModifierItem(Node):
    _children = ("expr", "alias")

    def __init__(self, expr: Node, alias: Optional[Node] = None):
        self.expr = expr
        self.alias = alias


class Alias(Node):
    _children = ("ident",)

    def __init__(self, ident: Node):
        self.ident = ident


class Ident(Node):
    _value = "value"

    def __init__(self, value: str):
        self.value = value


class PathExpression(Node):
    _children = ("components",)

    def __init__(self, components: list[Node]):
        self.components = components


class FromClause(Node):
    _children = ("expr",)

    def __init__(self, expr: Node):
        self.expr = expr


class TablePathExpression(Node):
    _children = ("path", "alias", "time_travel")

    def __init__(
        self, path: Node, alias: Optional[Node] = None, time_travel: Optional[Node] = None
    ):
        self.path = path
        self.alias = alias
        self.time_travel = time_travel


class TimeTravel(Node):
    _children = ("expr",)

    def __init__(self, expr: Node):
        self.expr = expr


class TableSubquery(Node):
    _children = ("query", "alias")

    def __init__(self, query: Node, alias: Optional[Node] = None):
        self.query = query
        self.alias = alias


class TableUnnestExpression(Node):
    _children = ("unnest_expr", "alias", "with_offset")

    def __init__(
        self, unnest_expr: Node, alias: Optional[Node] = None, with_offset: Optional[Node] = None
    ):
        self.unnest_expr = unnest_expr
        self.alias = alias
        self.with_offset = with_offset


class UnnestExpression(Node):
    _children = ("expr",)

    def __init__(self, expr: Node):
        self.expr = expr


class WithOffset(Node):
    _children = ("alias",)

    def __init__(self, alias: Optional[Node]):
        self.alias = alias


# Literals


class IntegerLiteral(Node):
    _value = "value"

    def __init__(self, value: str):
        self.value = value


# TODO: https://github.com/google/zetasql/blob/master/zetasql/public/strings.cc#L152
# Have fun!
class StringLiteral(Node):
    _value = "value"

    def __init__(self, value: str):
        self.value = value


class BytesLiteral(Node):
    _value = "value"

    def __init__(self, value: str):
        self.value = value


class NumericLiteral(Node):
    _value = "value"

    def __init__(self, value: str):
        self.value = value


class BigNumericLiteral(Node):
    _value = "value"

    def __init__(self, value: str):
        self.value = value


class FloatLiteral(Node):
    _value = "value"

    def __init__(self, value: str):
        self.value = value


class DateLiteral(Node):
    _value = "value"

    def __init__(self, value: str):
        self.value = value


class DatetimeLiteral(Node):
    _value = "value"

    def __init__(self, value: str):
        self.value = value


class TimestampLiteral(Node):
    _value = "value"

    def __init__(self, value: str):
        self.value = value


class RangeLiteral(Node):
    _value = "value"

    def __init__(self, value: str):
        self.value = value


class DateRangeLiteral(RangeLiteral):
    pass


class DatetimeRangeLiteral(RangeLiteral):
    pass


class TimestampRangeLiteral(RangeLiteral):
    pass


class JsonLiteral(Node):
    _value = "value"

    def __init__(self, value: str):
        self.value = value


class ArrayLiteral(Node):
    _children = ("elements",)

    def __init__(self, elements: list[Node]):
        self.elements = elements


class ArrayLiteralElement(Node):
    _children = ("expr",)

    def __init__(self, expr: Node):
        self.expr = expr


class StructLiteral(Node):
    _children = ("elements",)

    def __init__(self, elements: list[Node]):
        self.elements = elements


class StructLiteralElement(Node):
    _children = ("expr", "alias")

    def __init__(self, expr: Node, alias: Optional[Node] = None):
        self.expr = expr
        self.alias = alias


class BooleanLiteral(Node):
    _value = "value"

    def __init__(self, value: str):
        self.value = value


class NullLiteral(Node):
    _value = "value"

    def __init__(self):
        self.value = None
