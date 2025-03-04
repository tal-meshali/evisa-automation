from api.forms.arguments.argument import Arg


class BoolArg(Arg):
    VALIDATION_ERROR_MESSAGE = "value should be True or False"
    type = "bool"

    def _validate(self, val):
        return val in [True, False, "True", "False"]

    def parse_value(self):
        return False if self.value in [False, "False"] else True


class StringArg(Arg):
    VALIDATION_ERROR_MESSAGE = "value should be a string"
    type = "str"

    def _validate(self, val):
        return isinstance(val, str)


class NumberArg(Arg):
    VALIDATION_ERROR_MESSAGE = "value should be a number"
    type = "int"

    def _validate(self, val) -> bool:
        try:
            int(val)
            return True
        except TypeError:
            return False
