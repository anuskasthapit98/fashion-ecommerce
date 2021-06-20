from django import forms
from django.contrib.sessions.backends.base import CreateError
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

class CouponForm(FormControlMixin, ModelForm):
    class Meta:
        model = Coupon
        fields = '__all__'


class CheckoutForm(FormControlMixin, ModelForm):
    class Meta:
        model = Order
        fields = ["first_name","last_name","email","phone","company_name","province","address_one","address_two","zip_code",
                    "payment_method"]
