from django import forms
from product.models import Product, ProductWarehouse
from warehouse.models import Warehouse

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'merk', 'serial_number', 'size', 'color', 'cost_price', 'selling_price']
        labels = {
            "name": "Nama",
            "serial_number": "Seri",
            "size": "Ukuran",
            "color": "Warna",
            "cost_price": "Harga Beli",
            "selling_price": "Harga Jual",
        }