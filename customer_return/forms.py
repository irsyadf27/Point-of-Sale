from django import forms

class CustomerReturnForm(forms.Form):
    invoice_number = forms.CharField(label='No Invoice')  