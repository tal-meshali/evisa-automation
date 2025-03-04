from abc import abstractmethod, ABC

from django.db import models

from api.models.documents.document_validation import DocumentValidation
from api.models.documents.upload_status import UploadStatus
from api.visa_requests.pipelines.pipeline import Pipeline, ParsingException


class Document(models.Model):
    image = models.ImageField()
    upload_status = models.IntegerField(default=0)

    class Meta:
        abstract = True

    @property
    @abstractmethod
    def pipeline(self) -> Pipeline:
        pass

    def parse(self) -> DocumentValidation:
        try:
            self.upload_status = UploadStatus.Uploaded
            self.save()
            # result = self.pipeline.activate(self.image)
            self._parse()
            self.upload_status = UploadStatus.Valid
            return DocumentValidation(
                image=self.image,
                message=self.success_message,
                status=self.upload_status,
            )
        except ParsingException:
            self.upload_status = UploadStatus.Invalid
            self.image = None
            self.save()
            return DocumentValidation(
                image=self.image,
                message=",".join(self.pipeline.errors),
                status=self.upload_status,
            )

    @abstractmethod
    def _parse(self):
        return self.pipeline.activate(self.image)

    @property
    @abstractmethod
    def success_message(self) -> str:
        pass
