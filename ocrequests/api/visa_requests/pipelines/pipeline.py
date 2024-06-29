from ..stages.stage import Stage
from typing import List, Dict
from abc import ABC


class Pipeline(ABC):
    stages: List[Stage]
    name = None

    def activate(self, initial_input):
        if len(self.stages) == 0:
            return initial_input
        output = self.stages[0].run(initial_input)
        for stage in self.stages[1:]:
            output = stage.loop(output) if stage.should_loop else stage.run(output)
        return output


class MultiStagePipeline(Pipeline):
    pipelines: List[Pipeline]

    def __init__(self, should_duplicate: bool):
        self.should_duplicate = should_duplicate

    def activate(self, initial_input):
        pipeline_inputs = super().activate(initial_input)
        outputs = {}
        if self.should_duplicate:
            for pipeline in self.pipelines:
                self.update(outputs, pipeline, pipeline_inputs)
        else:
            if len(pipeline_inputs) != len(self.pipelines):
                raise ValueError("Output amount should match pipeline amount!")
            for pipeline_input, pipeline in zip(pipeline_inputs, self.pipelines):
                self.update(outputs, pipeline, pipeline_input)
        return outputs

    @staticmethod
    def update(update_into: Dict, pipeline: Pipeline, pipeline_input):
        pipeline_result = pipeline.activate(pipeline_input)
        if isinstance(pipeline_result, dict):
            update_into.update(**pipeline_result)
        else:
            update_into[pipeline.name] = pipeline_result
