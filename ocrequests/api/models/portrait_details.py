from django.db import models


def portrait_image_directory_path(instance, filename):
    return f"{instance.email_address}/portrait/{filename}"


class PortraitDetails(models.Model):
    portrait_image = models.ImageField(upload_to=portrait_image_directory_path)
