import re

from api.forms.arguments.argument import Arg

EMAIL_REGEX = r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"


class EmailAddressArg(Arg):
    VALIDATION_ERROR_MESSAGE = "mail should be of a valid format"
    type = "str"

    def _validate(self, val):
        return re.match(EMAIL_REGEX, val)
