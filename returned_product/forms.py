from django import forms
from product.models import Product, ProductWarehouse
from warehouse.models import Warehouse

class ReturnedProductForm(forms.ModelForm):
    product = forms.ModelChoiceField(label='Produk', queryset=Product.objects.all(), widget=forms.Select(attrs={'class':'js-matcher-returned form-control'})) 
    warehouse = forms.ModelChoiceField(label='Gudang', queryset=Warehouse.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    stock = forms.IntegerField(label='Gudang', widget=forms.NumberInput(attrs={'class':'form-control'})) 

    class Meta:
        model = ProductWarehouse
        fields = ['warehouse', 'product', 'stock']