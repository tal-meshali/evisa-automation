from visa_requests.pipelines.pipeline import Pipeline
from visa_requests.stages.dates import CreateDateStage, AddDaysToDateStage, ConvertDateToISOStage, \
    ConvertDateToRegularStage
from abc import ABC


class BasicDatePipeline(Pipeline, ABC):
    def __init__(self, include_iso: bool):
        if include_iso:
            self.stages.append(ConvertDateToISOStage())
        else:
            self.stages.append(ConvertDateToRegularStage())


class ArrivalDatePipeline(BasicDatePipeline):
    def __init__(self, include_iso: bool):
        self.stages = [CreateDateStage("%d/%m/%y")]
        super().__init__(include_iso)


class DepartureDatePipeline(BasicDatePipeline):
    def __init__(self, include_iso: bool):
        self.stages = [CreateDateStage("%d/%m/%y"), AddDaysToDateStage(14)]
        super().__init__(include_iso)


class PassportDatePipeline(BasicDatePipeline):
    def __init__(self, include_iso: bool):
        self.stages = []
        super().__init__(include_iso)
