import re

from api.forms.arguments.argument import Arg


class PhoneNumberArg(Arg):
    VALIDATION_ERROR_MESSAGE = "phone number is not valid"
    type = "str"

    def _validate(self, val):
        return re.match(r"05\d{8}", val) or re.match(r"\+9725\d{8}", val)
