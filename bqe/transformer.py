from lark import Transformer, Tree


class BqeTransformer(Transformer):
    def ident(self, args: list[Tree]):
        """Rewrite keyword_as_ident to ident"""
        child = args[0]
        if isinstance(child, Tree) and child.data == "keyword_as_ident":
            return Tree("ident", child.children)
        return Tree("ident", args)

    def query_expr(self, args: list[Tree]):
        """Collapse left-recursive query_expr"""
        if len(args) == 2:
            parent, child = args
            lhs, rhs = parent.children, [child]
            return Tree("query_expr", lhs + rhs)
        return Tree("query_expr", args)

    def field_access_expr(self, args: list[Tree]):
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
