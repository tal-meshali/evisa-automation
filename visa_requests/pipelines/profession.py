from visa_requests.pipelines.pipeline import Pipeline
from visa_requests.stages.profession import (
    DetermineProfessionStage
)


class ReceiveProfessionPipeline(Pipeline):
    def __init__(self):
        self.stages = [DetermineProfessionStage()]
