from django import forms
from .models import *


class FormControlMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class ProductForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = Products
        fields = "__all__"


class ProductImageForm()
