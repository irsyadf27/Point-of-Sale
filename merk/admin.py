from django.contrib import admin

from merk.models import Merk
from product.models import Product, ProductWarehouse
from received_product.models import ReceivedProduct, ReceivedProductDetail

# Register your models here.
admin.site.register(Merk)
admin.site.register(Product)
admin.site.register(ProductWarehouse)
admin.site.register(ReceivedProduct)
admin.site.register(ReceivedProductDetail)