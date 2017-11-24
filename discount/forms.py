from django import forms
from discount.models import Discount

class DiscountForm(forms.ModelForm):
    name = forms.CharField(required=True, label="Nama")
    
    class Meta:
        model = Discount
        fields = ['name', 'discount_type', 'discount_value']
        labels = {
            "discount_type": "Tipe Diskon",
            "discount_value": "Jumlah Diskon",
        }