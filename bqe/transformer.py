from lark import Transformer, Tree


def fixup_lrec_binary(args: list[Tree], name: str) -> Tree:
    """Fixup left-recursive binary trees. Returns a Tree named `name` with an n-ary list of children."""
    parent, child = args
    lhs, rhs = parent.children, child.children
    return Tree(name, lhs + rhs)


def coerce_binary(args: list[Tree]) -> list[Tree]:
    """Push a dummy node to guarantee that there are exactly two nodes in args."""
    next_args = [Tree("_noop", [])] + args
    return next_args[-2:]


class BqeTransformer(Transformer):
    def field_access_expr(self, args: list[Tree]):
        """Rewrite left-recursive field_access_expr to ident"""
        return fixup_lrec_binary(args, "ident")

    def path_expression(self, args: list[Tree]):
        """Rewrite left-recursive path_expression to ident"""
        return fixup_lrec_binary(coerce_binary(args), "ident")

    def grouping_set_list(self, args: list[Tree]):
        """Collapse left-recursive grouping_set_list"""
        return fixup_lrec_binary(coerce_binary(args), "grouping_set_list")

    def cube_list(self, args: list[Tree]):
        """Collapse left-recursive cube_list"""
        return fixup_lrec_binary(coerce_binary(args), "cube_list")

    def rollup_list(self, args: list[Tree]):
        """Collapse left-recursive rollup_list"""
        return fixup_lrec_binary(coerce_binary(args), "rollup_list")
