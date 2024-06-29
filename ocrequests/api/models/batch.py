from django.db import models
from django.contrib.auth.models import User


class Batch(models.Model):
    user = User()
    email_address = models.EmailField()
