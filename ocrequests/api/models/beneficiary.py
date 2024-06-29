from django.db import models
from ..models import PassportDetails, PortraitDetails, Batch


class Beneficiary(models.Model):
    passport = models.ForeignKey(PassportDetails, on_delete=models.CASCADE, null=True)
    portrait = models.ForeignKey(PortraitDetails, on_delete=models.CASCADE, null=True)
    full_name = models.CharField(max_length=30, null=True)
    related_batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True)
