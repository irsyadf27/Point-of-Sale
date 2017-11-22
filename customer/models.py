from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=250)
    phone = models.CharField(max_length=20)