from django.db import models


class PassportDetails(models.Model):
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    birth_place = models.CharField(max_length=10, null=True)
    passport_number = models.CharField(max_length=10, null=True)
    birth_date = models.DateField(max_length=10, null=True)
    issue_date = models.DateField(max_length=10, null=True)
    expiry_date = models.DateField(max_length=10, null=True)
    passport_image = models.ImageField()
