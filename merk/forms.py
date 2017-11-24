from django import forms
from merk.models import Merk

class MerkForm(forms.ModelForm):
    name = forms.CharField(required=True, label="Nama")
    
    class Meta:
        model = Merk
        fields = ['name']