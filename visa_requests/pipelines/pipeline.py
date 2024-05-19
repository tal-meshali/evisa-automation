from visa_requests.stages.stage import Stage
from typing import List
from abc import ABC


class Pipeline(ABC):
    stages: List[Stage]

    def activate(self, initial_input):
        output = self.stages[0].run(initial_input)
        for stage in self.stages[1:]:
            output = stage.loop(output) if stage.should_loop else stage.run(output)
        return output
