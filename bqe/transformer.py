from lark import Transformer, Tree


class BqeTransformer(Transformer):
    def field_access_expr(self, args: list[Tree]):
        """Rewrites left-recursive field_access_expr to ident"""
        parent, child = args
        lhs, rhs = parent.children, child.children
        return Tree("ident", lhs + rhs)

    def path_expression(self, args: list[Tree]):
        """Rewrites left-recursive path_expression to ident"""
        next_args = [Tree("_noop", [])] + args
        parent, child = next_args[-2:]
        lhs, rhs = parent.children, child.children
        return Tree("ident", lhs + rhs)
