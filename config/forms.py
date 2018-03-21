from django import forms
from config.models import Config

class ConfigForm(forms.ModelForm):
    class Meta:
        model = Config
        fields = ['potongan']