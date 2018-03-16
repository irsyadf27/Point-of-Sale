from django import forms
from django.contrib.auth.models import User

class AccountForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=False, label="Konfirmasi Password")
    first_name = forms.CharField(required=True, label="Nama Depan")
    last_name = forms.CharField(required=False, label="Nama Belakang")
    username = forms.CharField(required=True)
    email = forms.CharField(required=True)
    is_superuser = forms.CharField(widget=forms.CheckboxInput(), label="Admin", required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'is_superuser']

    def clean(self):
        cleaned_data = super(AccountForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Password dan Konfirmasi Password tidak sama."
            )

        if User.objects.filter(email__iexact=cleaned_data.get("email")).exclude(username=cleaned_data.get("username")).exists():
            raise forms.ValidationError(
                "Email sudah ada yang menggunakan."
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
    first_name = forms.CharField(required=True, label="Nama Depan")
    email = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=False, label="Konfirmasi Password")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean(self):
        cleaned_data = super(SettingForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Password dan Konfirmasi Password tidak sama."
            )

        if User.objects.filter(email__iexact=cleaned_data.get("email")).exclude(username=cleaned_data.get("username")).exists():
            raise forms.ValidationError(
                "Email sudah ada yang menggunakan."
            )

    def save(self, commit=True):
        user = super(SettingForm, self).save(commit=False)
        password = self.cleaned_data["password"]
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user