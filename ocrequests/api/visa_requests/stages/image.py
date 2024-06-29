from io import BytesIO
from sys import getsizeof

from ..stages.stage import Stage
from google.cloud import vision
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from abc import ABC


class VisionStage(Stage, ABC):
    def __init__(self, client: vision.ImageAnnotatorClient, should_loop=False):
        self.client = client
        super().__init__(should_loop)

    def run(self, stage_input: vision.Image):
        pass


class ConvertToVisionImageStage(Stage):
    def run(self, stage_input: InMemoryUploadedFile):
        content = stage_input.read()
        return stage_input, vision.Image(content=content)


class FaceDetectionStage(VisionStage):
    def run(self, stage_input):
        return (
            stage_input[0],
            self.client.face_detection(
                image=stage_input[1], max_results=1
            ).face_annotations[0],
        )  # pylint: disable=no-member


class PassportTextDetectionStage(VisionStage):
    def run(self, stage_input):
        return self.client.document_text_detection(
            image=stage_input[1]
        ).full_text_annotation


class CropImageStage(Stage):
    def run(self, stage_input):
        image, detection = stage_input
        image.seek(0)
        pil_image = Image.open(image)
        confidence = detection.detection_confidence
        width, height = pil_image.size
        [[x1, y1], [x2, y2]] = [
            (vertex.x, vertex.y)
            for index, vertex in enumerate(detection.bounding_poly.vertices)
            if index % 2 == 0
        ]
        if x2 - x1 < y2 - y1 and confidence > 0.9:
            addition = height * 0.1
            y1, y2 = max(0, y1 - addition), min(height, y2 + addition)
            diff = ((y2 - y1) * 0.75 - (x2 - x1)) / 2
            x1 -= diff
            x2 += diff
            return image, pil_image.crop((max(0, x1), y1, min(width, x2), y2))
        raise IOError("Image file isn't valid!")


class SaveImageValidFormatStage(Stage):
    def run(self, stage_input):
        original_image, cropped_image = stage_input
        buffer = BytesIO()
        cropped_image.save(
            fp=buffer, format=original_image.content_type.split("/")[1].upper()
        )
        buffer.seek(0)
        return InMemoryUploadedFile(
            buffer,
            "ImageField",
            original_image.name,
            "image/jpeg",
            getsizeof(buffer),
            None,
        )


class ReceiveWordListStage(Stage):
    def run(self, stage_input):
        word_list = []
        for page in stage_input.pages:
            for block in page.blocks:
                for paragraph in block.paragraphs:
                    for word in paragraph.words:
                        word_key = ""
                        for symbol in word.symbols:
                            word_key += symbol.text
                        word_list.append(word_key)
        return word_list
