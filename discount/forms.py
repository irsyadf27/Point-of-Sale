from django import forms
from discount.models import Discount

class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = ['name', 'discount_type', 'discount_value']
        labels = {
            "name": "Nama",
            "discount_type": "Tipe Diskon",
            "discount_value": "Jumlah Diskon",
        }