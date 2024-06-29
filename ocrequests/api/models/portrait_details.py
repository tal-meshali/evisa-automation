from django.db import models


class PortraitDetails(models.Model):
    portrait_image = models.ImageField()
