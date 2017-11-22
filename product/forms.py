from django import forms
from product.models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'merk', 'serial_number', 'size', 'color', 'price']
        labels = {
            "name": "Nama",
            "serial_number": "Seri",
            "size": "Ukuran",
            "color": "Warna",
            "price": "Harga",
        }