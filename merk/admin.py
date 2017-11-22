from django.contrib import admin

from merk.models import Merk
from product.models import Product

# Register your models here.
admin.site.register(Merk)
admin.site.register(Product)