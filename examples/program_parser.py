from typing import List, TypedDict, get_type_hints
from pyaskit import function


class AstNode(TypedDict):
    kind: str
    children: List["AstNode"]


@function(codable=False)
def parse(text: str) -> AstNode:
    """Parse the given {{text}} into an abstract syntax tree."""


def show_ast(node: AstNode, depth: int = 0) -> None:
    print("  " * depth + node["kind"])
    for child in node["children"]:
        show_ast(child, depth + 1)


ast = parse(
    """
def f(x: int) -> int:
    return x + 1
"""
)

show_ast(ast)
