class ConfigLanguageError(Exception):
    pass


class ParseError(ConfigLanguageError):
    pass


class EvaluationError(ConfigLanguageError):
    pass
