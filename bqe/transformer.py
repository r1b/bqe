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

    def path_expression(self, args: list[Tree]):
        """Collapse left-recursive path_expression"""
        if len(args) == 2:
            parent, child = args
            lhs, rhs = parent.children, [child]
            return Tree("path_expression", lhs + rhs)
        return Tree("path_expression", args)

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

    def grouping_set_list(self, args: list[Tree]):
        """Collapse left-recursive grouping_set_list"""
        if len(args) == 2:
            parent, child = args
            lhs, rhs = parent.children, [child]
            return Tree("grouping_set_list", lhs + rhs)
        return Tree("grouping_set_list", args)

    def cube_list(self, args: list[Tree]):
        """Collapse left-recursive cube_list"""
        if len(args) == 2:
            parent, child = args
            lhs, rhs = parent.children, [child]
            return Tree("cube_list", lhs + rhs)
        return Tree("cube_list", args)

    def rollup_list(self, args: list[Tree]):
        """Collapse left-recursive rollup_list"""
        if len(args) == 2:
            parent, child = args
            lhs, rhs = parent.children, [child]
            return Tree("rollup_list", lhs + rhs)
        return Tree("rollup_list", args)

    def named_struct_literal_item_list(self, args: list[Tree]):
        """Collapse left-recursive named_struct_literal_item_list"""
        if len(args) == 2:
            parent, child = args
            lhs, rhs = parent.children, [child]
            return Tree("named_struct_literal_item_list", lhs + rhs)
        return Tree("named_struct_literal_item_list", args)

    def pipe_selection_item_list(self, args: list[Tree]):
        """Collapse left-recursive pipe_selection_item_list"""
        if len(args) == 2:
            parent, child = args
            lhs, rhs = parent.children, [child]
            return Tree("pipe_selection_item_list", lhs + rhs)
        return Tree("pipe_selection_item_list", args)

    def pipe_selection_item_list_with_order(self, args: list[Tree]):
        """Collapse left-recursive pipe_selection_item_list_with_order"""
        if len(args) == 2:
            parent, child = args
            lhs, rhs = parent.children, [child]
            return Tree("pipe_selection_item_list_with_order", lhs + rhs)
        return Tree("pipe_selection_item_list_with_order", args)
