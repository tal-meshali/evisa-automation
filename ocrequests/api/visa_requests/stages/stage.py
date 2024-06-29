from abc import ABC, abstractmethod
from typing import List


class Stage(ABC):
    should_loop = False
    error_message: str = (
        "Failed to locate certain field, try to get a better capture of the document!"
    )

    def __init__(self, should_loop: bool = False):
        self.should_loop = should_loop

    @abstractmethod
    def run(self, stage_input):
        pass

    def loop(self, stage_input_list: List):
        return list(map(self.run, stage_input_list))
