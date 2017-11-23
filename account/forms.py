from django import forms
from django.contrib.auth.models import User

class AccountForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=False, label="Konfirmasi Password")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'is_superuser']
        labels = {
            "first_name": "Nama Depan",
            "last_name": "Nama Belakang",
            "username": "Username",
            "email": "Email",
        }

    def clean(self):
        cleaned_data = super(AccountForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Password dan Konfirmasi Password tidak sama."
            )

    def save(self, commit=True):
        user = super(AccountForm, self).save(commit=False)
        password = self.cleaned_data["password"]
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user

class SettingForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=False, label="Konfirmasi Password")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email',]
        labels = {
            "first_name": "Nama Depan",
            "last_name": "Nama Belakang",
            "email": "Email",
        }

    def clean(self):
        cleaned_data = super(SettingForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Password dan Konfirmasi Password tidak sama."
            )

    def save(self, commit=True):
        user = super(SettingForm, self).save(commit=False)
        password = self.cleaned_data["password"]
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user