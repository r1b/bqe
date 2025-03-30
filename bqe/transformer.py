from lark import Transformer, Tree


class BqeTransformer(Transformer):
    def field_access_expr(self, tree: Tree):
        """Rewrites left-recursive paths to ident"""
        lhs, rhs = tree
        return Tree('ident', lhs.children + rhs.children)