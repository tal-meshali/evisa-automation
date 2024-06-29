from django.db import models


def passport_image_directory_path(instance, filename):
    return f"{instance.email_address}/passport/{filename}"


class PassportDetails(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birth_place = models.CharField(max_length=10)
    passport_number = models.CharField(max_length=10)
    birth_date = models.DateField(max_length=10)
    issue_date = models.DateField(max_length=10)
    expiry_date = models.DateField(max_length=10)
    passport_image = models.ImageField(upload_to=passport_image_directory_path)
