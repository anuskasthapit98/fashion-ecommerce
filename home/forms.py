from django import forms
from django.contrib.sessions.backends.base import CreateError
from django.contrib.auth.forms import PasswordChangeForm
from django.forms import ModelForm


from dashboard.models import *
from dashboard.mixines import FormControlMixin

# newsletter


class SubscriptionForm(FormControlMixin, ModelForm):
    class Meta:
        model = Subscription
        fields = ['email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attr.update({
            'placeholder': 'Email Address'
        })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Subscription.objects.filter(email=email).exists():
            pass
        else:
            raise forms.ValidationError("User with this email doesn't exist")

        return email


class CustomerPasswordResetForm(FormControlMixin, forms.Form):

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter email address'
    }))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Customer.objects.filter(email=email).exists():
            pass
        else:
            raise forms.ValidationError("User with this email doesn't exist")

        return email


# password change form


class CustomerChangePasswordForm(PasswordChangeForm):
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


class CouponForm(FormControlMixin, ModelForm):
    class Meta:
        model = Coupon
        fields = '__all__'


class CheckoutForm(FormControlMixin, ModelForm):
    class Meta:
        model = Order
        fields = ["first_name", "last_name", "email", "phone", "company_name", "province", "address_one", "address_two", "zip_code",
                  "payment_method"]
