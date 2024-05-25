from ..pipelines.pipeline import Pipeline
from ..stages.passport_number import PassportNumberOptionsStage, FindMostProbableOptionStage


class PassportNumberPipeline(Pipeline):
    name = "passport_number"
    stages = [PassportNumberOptionsStage(), FindMostProbableOptionStage()]
