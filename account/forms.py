from django import forms
from django.contrib.auth.models import User

class AccountForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'is_superuser', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }
        labels = {
            "first_name": "Nama Depan",
            "last_name": "Nama Belakang",
            "username": "Username",
            "email": "Email",
        }