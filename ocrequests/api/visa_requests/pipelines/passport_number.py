from ..pipelines.pipeline import Pipeline
from ..stages.passport_number import PassportNumberOptionsStage, FindMostProbableOptionStage


class PassportNumberPipeline(Pipeline):
    stages = [PassportNumberOptionsStage(), FindMostProbableOptionStage()]
