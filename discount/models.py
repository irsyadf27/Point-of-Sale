from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Discount(models.Model):
    name = models.CharField(max_length=200)

    discount_type_choice = (
        ('percent', 'Percent'),
        ('cash', 'Cash'),
    )
    discount_type = models.CharField(
        max_length=10,
        choices=discount_type_choice,
    )
    discount_value = models.FloatField()

    @property
    def text(self):
        if self.discount_type == 'percent':
            return "%s%%" % self.discount_value
        else:
            return "Rp. %d" % int(self.discount_value)