from ..pipelines.pipeline import MultiStagePipeline
from ..stages.dates import CreateDateStage, FixUnknownDate, AcquireAllDatesStage, SortDatesStage
from ..stages.strings import (
    ScannedStringStage,
    FilterValidWordsOnlyStage
)
from ..pipelines.dates import PassportDatePipeline, FormatTypes
from typing import Dict
from ..pipelines.passport_number import PassportNumberPipeline
from ..pipelines.strings import SurnamePipeline, GivenNamePipeline, BirthPlacePipeline
from ..stages.image import ReceiveWordListStage, ConvertToVisionImageStage, PassportTextDetectionStage
from google.cloud.vision import ImageAnnotatorClient


class ReceiveRequiredStringsPipeline(MultiStagePipeline):
    stages = [FilterValidWordsOnlyStage(), ScannedStringStage(should_loop=True)]
    pipelines = [GivenNamePipeline(), SurnamePipeline(), BirthPlacePipeline()]

    def __init__(self):
        super().__init__(True)


class ReceiveRequiredDatesPipeline(MultiStagePipeline):
    stages = [AcquireAllDatesStage(), FixUnknownDate(should_loop=True),
              CreateDateStage("%d/%m/%Y", should_loop=True), SortDatesStage()]

    def __init__(self, names_and_formats: Dict[str, FormatTypes]):
        if len(names_and_formats.items()) != 3:
            raise ValueError("Should receive 3 pipelines for: Birth Date, Issue Date, Expiry Date!")
        self.pipelines = [PassportDatePipeline(name=name, _format=_format) for name, _format in
                          names_and_formats.items()]
        super().__init__(False)


class PassportDetailsPipeline(MultiStagePipeline):
    def __init__(self, client: ImageAnnotatorClient):
        self.pipelines = [ReceiveRequiredStringsPipeline(), ReceiveRequiredDatesPipeline({
            "birth_date": FormatTypes.NoFormat, "issue_date": FormatTypes.NoFormat,
            "expiry_date": FormatTypes.NoFormat}), PassportNumberPipeline()]
        self.stages = [ConvertToVisionImageStage(), PassportTextDetectionStage(client),
                       ReceiveWordListStage()]
        super().__init__(True)
