from django import forms

from .models import Product


class UpdateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description',)
