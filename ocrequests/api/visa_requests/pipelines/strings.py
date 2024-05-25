from ..pipelines.pipeline import Pipeline
from ..stages.strings import (
    FindResultUntilStopWordStage,
    StringFieldMatchStage,
    ScannedStringStage,
    GetFirstWordStage,
)


class GivenNamePipeline(Pipeline):
    name = "first_name"
    stages = [StringFieldMatchStage(["Given", "Name"], 2),
              FindResultUntilStopWordStage("Nationality", 3),
              ScannedStringStage()]


class SurnamePipeline(Pipeline):
    name = "last_name"
    stages = [StringFieldMatchStage(["Surname"], 2),
              FindResultUntilStopWordStage("Given", 1)]


class BirthPlacePipeline(Pipeline):
    name = "birth_place"
    stages = [StringFieldMatchStage(["Place", "of", "Birth"], 3),
              GetFirstWordStage()]
