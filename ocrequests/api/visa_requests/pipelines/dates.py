from ..pipelines.pipeline import Pipeline
from ..stages.dates import CreateDateStage, AddDaysToDateStage, ConvertDateToISOStage, \
    ConvertDateToRegularStage
from abc import ABC
from enum import Enum


class FormatTypes(Enum):
    ISO = 0,
    Regular = 1


class BasicDatePipeline(Pipeline, ABC):
    def __init__(self, _format: FormatTypes = None):
        if _format == FormatTypes.ISO:
            self.stages.append(ConvertDateToISOStage())
        elif _format == FormatTypes.Regular:
            self.stages.append(ConvertDateToRegularStage())


class ArrivalDatePipeline(BasicDatePipeline):
    stages = [CreateDateStage("%d/%m/%y")]


class DepartureDatePipeline(BasicDatePipeline):
    stages = [CreateDateStage("%d/%m/%y"), AddDaysToDateStage(14)]


class PassportDatePipeline(BasicDatePipeline):
    stages = []
