from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from warehouse.models import Warehouse
from product.models import Product

# Create your models here.
class LogsStock(models.Model):
    actor = models.ForeignKey(User)
    created_at = models.DateTimeField(default=timezone.now)
    warehouse = models.ForeignKey(Warehouse)
    product = models.ForeignKey(Product)
    stock = models.IntegerField()