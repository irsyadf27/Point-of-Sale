from django.contrib import admin

from merk.models import Merk
from product.models import Product, ProductWarehouse
from received_product.models import ReceivedProduct, ReceivedProductDetail
from cashier.models import Invoice, InvoiceDetail

# Register your models here.
admin.site.register(Merk)
admin.site.register(Product)
admin.site.register(ProductWarehouse)
admin.site.register(ReceivedProduct)
admin.site.register(ReceivedProductDetail)
admin.site.register(Invoice)
admin.site.register(InvoiceDetail)