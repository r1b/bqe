from enum import auto, IntEnum
from lark import Token
from lark.lark import PostLex
from typing import Iterator, Iterable


class PostLexMode(IntEnum):
    """
    Postlex modes:

    - NORMAL: Accept tokens immediately
    - JOIN_KW_DISAMBIGUATION: Defer JOIN tokens until we have more context
    """

    NORMAL = auto()
    JOIN_KW_DISAMBIGUATION = auto()


class BqePostLexState:
    """Helper for postlex state."""

    def __init__(self):
        self.buf = []
        self.mode = PostLexMode.NORMAL

    def defer(self, token: Token):
        self.buf.append(token)

    def flush(self) -> Iterable[Token]:
        yield from self.buf
        self.buf = []


class BqePostLex(PostLex):
    """
    Lexer postprocessing.

    AMBIGUOUS CASE 1: JOIN keywords
        > SELECT 1 AS x |> LEFT OUTER UNION ALL SELECT 2 AS x
        INNER, FULL and LEFT can appear before both set operations and JOINs
        Resolved by rewriting JOIN keywords to set-operation-specific variants
        when a set-operation keyword follows.
        Ref: https://github.com/google/zetasql/blob/2025.03.1/zetasql/parser/lookahead_transformer.cc#L754-L755
    """

    def process(self, stream: Iterator[Token]) -> Iterator[Token]:
        state = BqePostLexState()

        for token in stream:
            if state.mode == PostLexMode.NORMAL:
                yield from self.process_normal(token, state)
            elif state.mode == PostLexMode.JOIN_KW_DISAMBIGUATION:
                yield from self.process_join_kw_disambiguation(token, state)

        yield from state.flush()

    def process_normal(self, token: Token, state: BqePostLexState):
        if token.type in ("FULL", "INNER", "LEFT"):
            state.mode = PostLexMode.JOIN_KW_DISAMBIGUATION
            state.defer(token)
        else:
            yield token

    def process_join_kw_disambiguation(self, lookahead: Token, state: BqePostLexState):
        if lookahead.type == "OUTER":
            state.defer(lookahead)
            return

        if lookahead.type in ("EXCEPT", "INTERSECT", "UNION"):
            yield from self.rewrite_join_kw_tokens(state)
        else:
            yield from state.flush()

        state.mode = PostLexMode.NORMAL
        yield lookahead

    def rewrite_join_kw_tokens(self, state: BqePostLexState):
        for token in state.flush():
            if token.type == "FULL":
                yield Token("FULL_IN_SET_OPERATION", token.value)
            elif token.type == "INNER":
                yield Token("INNER_IN_SET_OPERATION", token.value)
            elif token.type == "LEFT":
                yield Token("LEFT_IN_SET_OPERATION", token.value)
            else:
                yield token
