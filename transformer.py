from lark import Transformer, Token
from errors import EvaluationError


class ConfigTransformer(Transformer):
    def __init__(self):
        super().__init__()
        self.constants = {}

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
        return {"name": name, "value": value}

    def expression_statement(self, items):
        return items[0]

    def start(self, items):
        return items