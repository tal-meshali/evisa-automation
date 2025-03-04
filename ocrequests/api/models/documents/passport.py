from django.db import models

from api.models.documents.document import Document
from api.utility.client import client
from api.visa_requests.pipelines.general import PassportDetailsPipeline
from api.visa_requests.pipelines.pipeline import Pipeline


class Passport(Document):
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    birth_place = models.CharField(max_length=10, null=True)
    passport_number = models.CharField(max_length=10, null=True)
    birth_date = models.DateField(max_length=10, null=True)
    issue_date = models.DateField(max_length=10, null=True)
    expiry_date = models.DateField(max_length=10, null=True)

    @property
    def pipeline(self) -> Pipeline:
        return PassportDetailsPipeline(client)

    def _parse(self):
        result = super()._parse()
        for key in result:
            setattr(self, key, result[key])
        self.save()

    @property
    def success_message(self) -> str:
        return f"{self.first_name} {self.last_name}"
