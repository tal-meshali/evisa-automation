from abc import abstractmethod, ABC

from api.forms.validation.validation_result import ValidationResult
from api.forms.visiblity.arg_visibility import Visibility


class Arg(ABC):
    VALIDATION_ERROR_MESSAGE: str = ""
    type: str = ""

    def __init__(
        self,
        name: str,
        value=None,
        required=True,
        visibility: Visibility = None,
        description: str = None,
    ):
        self.name = name
        self.value = value
        self.description = description
        self.required = required
        self.visibility = visibility

    def validate(self, val) -> ValidationResult:
        valid = self._validate(val)
        return (
            ValidationResult(True)
            if valid
            else ValidationResult(False, self.VALIDATION_ERROR_MESSAGE)
        )

    @abstractmethod
    def _validate(self, val) -> bool:
        pass

    def update_value(self, val):
        validation = self.validate(val)
        if not validation:
            self.value = val
            return None
        return validation

    def parse_value(self):
        return str(self.value)

    def structure(self):
        return {
            "name": self.name,
            "type": self.type,
            "required": self.required,
            "value": self.value,
            "description": self.description,
        }
