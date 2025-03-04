from api.models.documents.document import Document
from api.utility.client import client
from api.visa_requests.pipelines.image import PortraitImagePipeline
from api.visa_requests.pipelines.pipeline import Pipeline


class Portrait(Document):
    def pipeline(self) -> Pipeline:
        return PortraitImagePipeline(client)

    @property
    def success_message(self) -> str:
        return "Parsed image successfully"

    def _parse(self):
        result = super()._parse()
        self.image = result
        self.save()
