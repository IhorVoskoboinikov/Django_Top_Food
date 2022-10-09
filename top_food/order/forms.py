from django import forms


class OrderForm(forms.Form):
    first_dish = forms.CharField(max_length=1000)
    second_dish = forms.CharField(max_length=1000)
    drinks = forms.CharField(max_length=1000)
    other = forms.CharField(max_length=1000)
