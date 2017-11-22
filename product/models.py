from __future__ import unicode_literals

from django.db import models
from merk.models import Merk
from warehouse.models import Warehouse

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    merk = models.ForeignKey(Merk, related_name='products')
    serial_number = models.CharField(max_length=200)
    choice_size = (
        ('40x30', '40x30'),
        ('30x40', '30x40'),
        ('60x60', '60x60'),
    )
    size = models.CharField(
        max_length=10,
        choices=choice_size,
    )
    color = models.CharField(max_length=15)
    price = models.FloatField()

    def __unicode__(self):
        return "%s (%s) %s" % (self.name, self.size, self.color)

class ProductWarehouse(models.Model):
    warehouse = models.ForeignKey(Warehouse, related_name='products')
    product = models.ForeignKey(Product, related_name='warehouse')
    stock = models.IntegerField()