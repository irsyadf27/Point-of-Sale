from django import forms

class CashierForm(forms.Form):
    product = forms.ChoiceField(label='Produk', widget=forms.Select(attrs={'class':'js-matcher-kasir form-control'})) 
    qty = forms.IntegerField(label='QTY', widget=forms.NumberInput(attrs={'class':'form-control', 'value': 1, 'id': 'qty-product'})) 