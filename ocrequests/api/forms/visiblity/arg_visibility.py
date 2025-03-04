from typing import Dict, Any


class Visibility:
    def __init__(self, arg_name, arg_value):
        self.arg_name = arg_name
        self.arg_value = arg_value

    def is_visible(self, args_dict: Dict[str, Any]):
        return args_dict[self.arg_name] == self.arg_value
