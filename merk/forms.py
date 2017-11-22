from django import forms
from merk.models import Merk

class MerkForm(forms.ModelForm):
    class Meta:
        model = Merk
        fields = ['name']
        labels = {
            "name": "Nama",
        }