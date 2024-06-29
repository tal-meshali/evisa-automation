from django.core.files.uploadedfile import InMemoryUploadedFile
from ..pipelines.pipeline import Pipeline
from ..stages.image import (
    ConvertToVisionImageStage,
    FaceDetectionStage,
    CropImageStage,
    PassportTextDetectionStage,
    ReceiveWordListStage,
    SaveImageValidFormatStage,
)
from google.cloud.vision import ImageAnnotatorClient


class PortraitImagePipeline(Pipeline):
    def __init__(self, client: ImageAnnotatorClient):
        self.stages = [
            ConvertToVisionImageStage(),
            FaceDetectionStage(client),
            CropImageStage(),
            SaveImageValidFormatStage(),
        ]


class PassportImagePipeline(Pipeline):
    def __init__(self, client: ImageAnnotatorClient):
        self.stages = [
            ConvertToVisionImageStage(),
            PassportTextDetectionStage(client),
            ReceiveWordListStage(),
        ]
