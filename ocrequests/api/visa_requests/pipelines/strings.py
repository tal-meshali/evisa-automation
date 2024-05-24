from ..pipelines.pipeline import Pipeline
from ..stages.strings import (
    FindResultUntilStopWordStage,
    StringFieldMatchStage,
    ScannedStringStage,
    GetFirstWordStage,
)


class GivenNamePipeline(Pipeline):
    stages = [StringFieldMatchStage(["Given", "Name"], 2),
              FindResultUntilStopWordStage("Nationality", 3),
              ScannedStringStage()]


class SurnamePipeline(Pipeline):
    stages = [StringFieldMatchStage(["Surname"], 2),
              FindResultUntilStopWordStage("Given", 1)]


class BirthPlacePipeline(Pipeline):
    stages = [StringFieldMatchStage(["Place", "of", "Birth"], 3),
              GetFirstWordStage()]
