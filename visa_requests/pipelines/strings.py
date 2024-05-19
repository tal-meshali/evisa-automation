from visa_requests.pipelines.pipeline import Pipeline
from visa_requests.stages.strings import (
    FindResultUntilStopWordStage,
    StringFieldMatchStage,
    ScannedStringStage,
    GetFirstWordStage,
)


class GivenNamePipeline(Pipeline):
    def __init__(self):
        self.stages = [StringFieldMatchStage(["Given", "Name"], 2),
                       FindResultUntilStopWordStage("Nationality", 3),
                       ScannedStringStage()]


class SurnamePipeline(Pipeline):
    def __init__(self):
        self.stages = [StringFieldMatchStage(["Surname"], 2),
                       FindResultUntilStopWordStage("Given", 1)]


class BirthPlacePipeline(Pipeline):
    def __init__(self):
        self.stages = [StringFieldMatchStage(["Place", "of", "Birth"], 3),
                       GetFirstWordStage()]
