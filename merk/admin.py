from django.contrib import admin

from merk.models import Merk
from product.models import Product, ProductWarehouse
from received_product.models import ReceivedProduct, ReceivedProductDetail
from cashier.models import Invoice, InvoiceDetail
from config.models import Config
from customer_return.models import Retur, ReturDetail

# Register your models here.
admin.site.register(Merk)
admin.site.register(Product)
admin.site.register(ProductWarehouse)
admin.site.register(ReceivedProduct)
admin.site.register(ReceivedProductDetail)
admin.site.register(Invoice)
admin.site.register(InvoiceDetail)
admin.site.register(Config)
admin.site.register(Retur)
admin.site.register(ReturDetail)