from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Config(models.Model):
    potongan = models.FloatField(default=5000)