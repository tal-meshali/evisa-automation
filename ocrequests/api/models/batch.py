from django.db import models
from django.contrib.auth.models import User


class Batch(models.Model):
    user = User()
    email_address = models.EmailField()
    ready_to_parse = models.BooleanField(default=False)
    arrival_date = models.DateField()
    departure_date = models.DateField()
