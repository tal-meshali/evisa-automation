from ocrequests.api.visa_requests.pipelines.pipeline import Pipeline
from ocrequests.api.visa_requests.stages.profession import DetermineProfessionStage


class ReceiveProfessionPipeline(Pipeline):
    stages = [DetermineProfessionStage()]
