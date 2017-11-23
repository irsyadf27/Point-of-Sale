from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Merk(models.Model):
    name = models.CharField(max_length=60)

    def __unicode__(self):
        return self.name
        
    @property
    def num_of_products(self):
        return self.products.count()