from __future__ import unicode_literals
from django.db import models
from django.db.models import Count
from product.models import Product, ProductWarehouse
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Invoice(models.Model):
    invoice_number = models.CharField(max_length=128, blank=False, unique=True)
    qty = models.IntegerField()
    cashier = models.ForeignKey(User, related_name='invoice_by')
    created_at = models.DateTimeField(default=timezone.now)
    total = models.FloatField(blank=True, default=None)

    def __str__(self):
        return "%s" % (self.invoice_number)

    def __unicode__(self):
        return "%s" % (self.invoice_number)

    def generate_invoice_number(self):
        month = timezone.datetime.now().month
        year = timezone.datetime.now().year
        total = Invoice.objects.filter(created_at__year=year, created_at__month=month).count()
        return 'INV-%s%s%0.6d' % (year, month, total + 1)

    def save(self):
        if not self.pk :
           ### we have a newly created object, as the db id is not set
           self.invoice_number = self.generate_invoice_number()
        super(Invoice , self).save()

class InvoiceDetail(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='details')
    product_warehouse = models.ForeignKey(ProductWarehouse)
    qty = models.IntegerField()
    price = models.FloatField(blank=True, default=None)
    subtotal = models.FloatField(blank=True, default=None)