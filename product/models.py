from __future__ import unicode_literals

from django.db import models
from merk.models import Merk
from warehouse.models import Warehouse
import qrcode
import uuid
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


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
    cost_price = models.FloatField(blank=True, default=None)
    selling_price = models.FloatField(blank=True, default=None)
    qrcode = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    
    def __str__(self):
        return "%s Seri %s (%s) %s" % (self.name, self.serial_number, self.size, self.color)

    def __unicode__(self):
        return "%s Seri %s (%s) %s" % (self.name, self.serial_number, self.size, self.color)

    @property
    def generate_qrcode(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=6,
            border=0,
        )
        qr.add_data(self.qrcode)
        qr.make(fit=True)
        img = qr.make_image()
        output = StringIO()
        img.save(output, "PNG")
        contents = output.getvalue().encode("base64")
        output.close()
        return contents

class ProductWarehouse(models.Model):
    warehouse = models.ForeignKey(Warehouse, related_name='products')
    product = models.ForeignKey(Product, related_name='warehouse')
    stock = models.IntegerField()

    #class Meta:
    #    unique_together = ('warehouse', 'product')