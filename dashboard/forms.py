from django import forms
from .models import *

from django.contrib.auth.forms import PasswordChangeForm


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].widget.attrs.update({
            'class': "control outlined control-checkbox checkbox-success"
        })


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']


class StaffLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))


class PasswordResetForm(forms.Form):

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter email address'
    }))

    def clean_email(self):
        e = self.cleaned_data.get('email')
        if Account.objects.filter(email=e).exists():
            pass
        else:
            raise forms.ValidationError("User with this email doesn't exist")

        return e


class ChangePasswordForm(PasswordChangeForm):
    old_password_flag = True

    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder':  'Old Password'}))

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder':  'New Password'}))

    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder':  'New Password again'}))

    def set_user(self, user):
        self.user = user

    def clean(self):
        old_password = self.cleaned_data.get('old_password')
        valpwd = self.cleaned_data.get('new_password1')
        valrpwd = self.cleaned_data.get('new_password2')

        if valpwd != valrpwd:
            raise forms.ValidationError({
                'new_password1': 'Password Not Matched'})

        else:
            pass
        return self.cleaned_data
