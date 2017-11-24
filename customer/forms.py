from django import forms
from customer.models import Customer

class CustomerForm(forms.ModelForm):
    name = forms.CharField(required=True, label="Nama")
    address = forms.CharField(required=True, label="Alamat")
    phone = forms.CharField(required=False, label="No. Telp/HP")

    class Meta:
        model = Customer
        fields = ['name', 'address', 'phone']