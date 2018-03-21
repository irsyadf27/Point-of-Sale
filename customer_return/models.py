from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from product.models import ProductWarehouse
from cashier.models import Invoice

# Create your models here.
class Retur(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='retur')
    cashier = models.ForeignKey(User, related_name='retur_by')
    created_at = models.DateTimeField(default=timezone.now)
    qty = models.IntegerField()
    potongan = models.FloatField(blank=True, default=None)
    total = models.FloatField(blank=True, default=None)

class ReturDetail(models.Model):
    retur = models.ForeignKey(Retur, related_name='details')
    product_warehouse = models.ForeignKey(ProductWarehouse)
    qty = models.IntegerField()
    selling_price = models.FloatField(blank=True, default=None)
    subtotal = models.FloatField(blank=True, default=None)