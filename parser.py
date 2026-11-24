
from lark import Lark, Transformer
from lark.exceptions import LarkError, VisitError

from errors import ParseError, EvaluationError


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


class ConfigTransformer(Transformer):

    def __init__(self):
        super().__init__()
        self.constants = {}

    def statement(self, items):
        return items[0]

    def number(self, items):
        return int(items[0])

    def variable(self, items):
        name = str(items[0])

        if name not in self.constants:
            raise EvaluationError(f"Undefined constant: {name}")

        return self.constants[name]

    def array(self, items):
        return list(items)

    def add(self, items):
        return items[0] + items[1]

    def subtract(self, items):
        return items[0] - items[1]

    def max_func(self, items):
        return max(items[0], items[1])

    def mod_func(self, items):
        if items[1] == 0:
            raise EvaluationError("Division by zero in mod()")

        return items[0] % items[1]

    def calculation(self, items):
        return items[0]

    def constant(self, items):
        name = str(items[0])
        value = items[1]

        self.constants[name] = value

        return {
            "name": name,
            "value": value
        }

    def expression_statement(self, items):
        return items[0]

    def start(self, items):
        return items


def parse_text(text):
    try:
        tree = parser.parse(text)
        transformer = ConfigTransformer()
        return transformer.transform(tree)

    except VisitError as error:
        if isinstance(error.orig_exc, EvaluationError):
            raise error.orig_exc from error

        raise ParseError(str(error.orig_exc)) from error

    except LarkError as error:
        raise ParseError(str(error)) from error
