from visa_requests.pipelines.pipeline import Pipeline
from visa_requests.stages.dates import CreateDateStage, FixUnknownDate, AcquireAllDatesStage, SortDatesStage
from visa_requests.stages.strings import (
    ScannedStringStage,
    FilterValidWordsOnlyStage
)


class InitialWordListPipeline(Pipeline):
    def __init__(self):
        self.stages = [FilterValidWordsOnlyStage(), ScannedStringStage(should_loop=True)]


class ReceiveRequiredDatesPipeline(Pipeline):
    def __init__(self):
        self.stages = [AcquireAllDatesStage(), FixUnknownDate(should_loop=True),
                       CreateDateStage("%d/%m/%Y", should_loop=True), SortDatesStage()]
