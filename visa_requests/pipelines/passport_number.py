from visa_requests.pipelines.pipeline import Pipeline
from visa_requests.stages.passport_number import PassportNumberOptionsStage, FindMostProbableOptionStage


class PassportNumberPipeline(Pipeline):
    def __init__(self):
        self.stages = [PassportNumberOptionsStage(), FindMostProbableOptionStage()]
