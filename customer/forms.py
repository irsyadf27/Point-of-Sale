from django import forms
from customer.models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'address', 'phone']
        labels = {
            "name": "Nama",
            "address": "Alamat",
            "phone": "No. Telp/HP",
        }