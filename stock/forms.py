from django import forms
from product.models import ProductWarehouse

class ProductWarehouseForm(forms.ModelForm):
    class Meta:
        model = ProductWarehouse
        fields = ['warehouse', 'product', 'stock']
        labels = {
            "warehouse": "Gudang",
            "product": "Produk",
            "stock": "Stok",
        }