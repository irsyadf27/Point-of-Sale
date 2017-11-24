from django import forms
from product.models import Product, ProductWarehouse
from warehouse.models import Warehouse

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'merk', 'serial_number', 'size', 'color', 'purchase_price', 'selling_price']
        labels = {
            "name": "Nama",
            "serial_number": "Seri",
            "size": "Ukuran",
            "color": "Warna",
            "purchase_price": "Harga Beli",
            "selling_price": "Harga Jual",
        }

class IncomeProductForm(forms.ModelForm):
    product = forms.ModelChoiceField(label='Produk', queryset=Product.objects.all(), widget=forms.Select(attrs={'class':'js-example-matcher-start form-control'})) 
    warehouse = forms.ModelChoiceField(label='Gudang', queryset=Warehouse.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    stock = forms.IntegerField(label='Gudang', widget=forms.NumberInput(attrs={'class':'form-control'})) 

    class Meta:
        model = ProductWarehouse
        fields = ['warehouse', 'product', 'stock']


    def save(self, commit=False):
        obj, created  = ProductWarehouse.objects.get_or_create(warehouse=self.cleaned_data["warehouse"], product=self.cleaned_data["product"], defaults={"stock": 0})
        obj.stock += self.cleaned_data["stock"]
        obj.save()
        return obj