from django.db import models


class PassportDetails(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birth_place = models.CharField(max_length=10)
    passport_number = models.CharField(max_length=10)
    birth_date = models.DateField(max_length=10)
    issue_date = models.DateField(max_length=10)
    expiry_date = models.DateField(max_length=10)
    passport_image = models.ImageField()
