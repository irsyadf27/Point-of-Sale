from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Warehouse(models.Model):
    name = models.CharField(max_length=60)
    address = models.CharField(max_length=250)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    @property
    def num_of_products(self):
        return self.products.count()