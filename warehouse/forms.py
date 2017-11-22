from django import forms
from warehouse.models import Warehouse

class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ['name', 'address', 'phone']
        labels = {
            "name": "Nama",
            "address": "Alamat",
            "phone": "No. Telp/HP",
        }