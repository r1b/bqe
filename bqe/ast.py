from typing import Optional


def pretty(node: "Node", indent="  ", nl="\n"):
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
            args.append(str(value))

        if node._options:
            for option_name in node._options:
                option = getattr(node, option_name)
                if option is not None:
                    args.append(f"{option_name}={str(option)}")

        if args:
            result += "(" + ", ".join(args) + ")"

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
    _children: tuple[Optional[str], ...] = ()
    _options: tuple[Optional[str], ...] = ()
    _value: Optional[str] = None


class Query(Node):
    _children = ("query_expr", "pipe_exprs")

    def __init__(self, query_expr: Node, pipe_exprs: Optional[list[Node]] = None):
        self.query_expr = query_expr
        self.pipe_exprs = pipe_exprs


class Select(Node):
    _children = ("select_list", "from_clause")
    _options = ("distinct",)

    def __init__(
        self,
        select_list: Node,
        from_clause: Optional[Node] = None,
        distinct: Optional[bool] = False,
    ):
        self.select_list = select_list
        self.from_clause = from_clause
        self.distinct = distinct


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


class Alias(Node):
    _children = ("ident",)

    def __init__(self, ident: Node):
        self.ident = ident


class Ident(Node):
    _value = "value"

    def __init__(self, value: str):
        self.value = value


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
