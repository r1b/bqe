from lark import Transformer, Tree


def fixup_lrec_rule(args: list[Tree], name: str, spread=True) -> Tree:
    """Fixup left-recursive rules. Returns a Tree named `name` with a list of all leaves collected
    from the children of the RHS. If `spread` is `False`, the RHS will be preserved along with its children.
    """
    parent, child = args
    lhs, rhs = parent.children, child.children if spread else [child]
    return Tree(name, lhs + rhs)


def coerce_binary(args: list[Tree]) -> list[Tree]:
    """Push a dummy node to guarantee that there are exactly two nodes in `args`."""
    next_args = [Tree("_noop", [])] + args
    return next_args[-2:]


class BqeTransformer(Transformer):
    def query_expr(self, args: list[Tree]):
        """Collapse left-recursive query_expr"""
        return fixup_lrec_rule(coerce_binary(args), "query_expr", spread=False)

    def path_expression(self, args: list[Tree]):
        """Rewrite left-recursive path_expression to ident"""
        return fixup_lrec_rule(coerce_binary(args), "ident")

    def grouping_set_list(self, args: list[Tree]):
        """Collapse left-recursive grouping_set_list"""
        return fixup_lrec_rule(coerce_binary(args), "grouping_set_list")

    def cube_list(self, args: list[Tree]):
        """Collapse left-recursive cube_list"""
        return fixup_lrec_rule(coerce_binary(args), "cube_list")

    def rollup_list(self, args: list[Tree]):
        """Collapse left-recursive rollup_list"""
        return fixup_lrec_rule(coerce_binary(args), "rollup_list")

    def named_struct_literal_item_list(self, args: list[Tree]):
        """Collapse left-recursive named_struct_literal_item_list"""
        return fixup_lrec_rule(coerce_binary(args), "named_struct_literal_item_list", spread=False)
