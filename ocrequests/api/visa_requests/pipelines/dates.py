from ..pipelines.pipeline import Pipeline
from ..stages.dates import CreateDateStage, AddDaysToDateStage, ConvertDateToISOStage, \
    ConvertDateToRegularStage, ConvertToBothDateFormsStage
from abc import ABC
from enum import Enum


class FormatTypes(Enum):
    ISO = 0,
    Regular = 1
    Both = 2


class BasicDatePipeline(Pipeline, ABC):
    def __init__(self, _format: FormatTypes = None):
        if _format == FormatTypes.ISO:
            self.stages.append(ConvertDateToISOStage())
        elif _format == FormatTypes.Regular:
            self.stages.append(ConvertDateToRegularStage())
        elif _format == FormatTypes.Both:
            self.stages.append(ConvertToBothDateFormsStage())


class ArrivalDatePipeline(BasicDatePipeline):
    stages = [CreateDateStage("%d/%m/%y")]


class DepartureDatePipeline(BasicDatePipeline):
    stages = [CreateDateStage("%d/%m/%y"), AddDaysToDateStage(14)]


class PassportDatePipeline(BasicDatePipeline):
    stages = []
