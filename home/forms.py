from django import forms
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
        print(email,'11111111111111111111111111111111111')
        if Customer.objects.filter(email=email).exists():
            pass
        else:
            raise forms.ValidationError("User with this email doesn't exist")

        return email



    