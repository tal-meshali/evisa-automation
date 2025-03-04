import datetime

from api.forms.arguments.argument import Arg


class DateArg(Arg):
    type = "date"

    def __init__(self, date_format: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.date_format = date_format or "%d/%m/%y"
        self.VALIDATION_ERROR_MESSAGE = f"date should match format {self.date_format}"

    def _validate(self, val):
        try:
            datetime.datetime.strptime(self.value, self.date_format)
            return True
        except ValueError:
            return False

    def parse_value(self):
        return datetime.datetime.strptime(self.value, self.date_format)

    def structure(self):
        return {"date_format": self.date_format, **super().structure()}
