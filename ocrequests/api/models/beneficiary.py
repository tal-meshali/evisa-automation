from django.db import models

from .documents.passport import Passport
from .documents.portrait import Portrait
from ..models import Batch


class Beneficiary(models.Model):
    passport = models.OneToOneField(Passport, on_delete=models.CASCADE, null=True)
    portrait = models.OneToOneField(Portrait, on_delete=models.CASCADE, null=True)
    batch = models.ForeignKey(
        Batch, on_delete=models.SET_NULL, null=True, related_name="beneficiaries"
    )

    def save_item(self, item: models.Model):
        item.beneficiary = self
        self.save()
        item.save()
