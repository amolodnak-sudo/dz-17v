from lark import Lark
from lark.exceptions import LarkError
from errors import ParseError
from transformer import ConfigTransformer


GRAMMAR = r"""
    start: statement*

    statement: constant
             | expression_statement

    constant: NAME "<-" value

    expression_statement: value

    ?value: NUMBER              -> number
          | array
          | calculation

    array: "(" "list" value* ")"

    calculation: "^{" expr "}"

    ?expr: expr "+" term       -> add
         | expr "-" term       -> subtract
         | term

    ?term: function
         | atom

    ?atom: NUMBER              -> number
         | NAME                -> variable
         | "(" expr ")"

    function: "max" "(" expr "," expr ")"  -> max_func
            | "mod" "(" expr "," expr ")"  -> mod_func

    NAME: /[A-Z]+/
    NUMBER: /[+-]?(?:[1-9][0-9]*|0)/

    COMMENT: /(?s:\/\*.*?\*\/)/
    %ignore COMMENT
    %ignore WS

    WS: /[ \t\f\r\n]+/
"""

parser = Lark(GRAMMAR, parser="lalr")


def parse_text(text):
    try:
        tree = parser.parse(text)
        transformer = ConfigTransformer()
        return transformer.transform(tree)
    except LarkError as error:
        raise ParseError(str(error)) from error