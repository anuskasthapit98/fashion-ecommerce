from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordChangeForm

from .mixin import *
from .models import *

# user create form


class UserForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = Account
        fields = ['username', 'email', 'address', 'image', 'mobile', 'groups']
        widgets = {
            'image': forms.ClearableFileInput(attrs={
                'onchange': 'preview()'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['groups'].widget.attrs.update(
            {'class': 'form-control select2 feature-select'})

    def clean(self):
        cleaned_data = super().clean()
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        mobile = self.cleaned_data['mobile']
        if Account.objects.filter(username=username).exists():
            raise ValidationError({
                'username': 'this username is not available'
            })
        if Account.objects.filter(email=email).exists():
            raise ValidationError({
                'email': 'user with this email already exists'
            })
        if Account.objects.filter(mobile=mobile):
            raise ValidationError({
                'mobile': 'user with this mobile no. already exists'
            })
        if len(mobile) < 10:
            raise ValidationError({
                'mobile': 'Invalid mobile no.'
            })


# login form
class StaffLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))

    def clean(self):
        cleaned_data = super().clean()
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            pass
        else:
            raise ValidationError({
                'username': 'Invalid username or password'
            })

# password reset form


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

# password change form


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

# category create form


class CategoryForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"

    def clean_slug(self):
        slug = self.cleaned_data['slug']

        if Category.objects.filter(slug=slug).exists():
            raise forms.ValidationError('This ID is not available')
        else:
            pass

        return slug

# product image form


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']

# product create form


class ProductForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = Products
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].widget.attrs.update({
            'class': "control outlined control-checkbox checkbox-success"
        })
        self.fields['vat_incl'].widget.attrs.update({
            'class': "control outlined control-checkbox checkbox-success"
        })
        self.fields['size'].widget.attrs.update({
            'class': 'form-control select2'
        })

# brand create form


class BrandForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = Brands
        fields = "__all__"
        widgets = {
            'brand_logo': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'placeholder': 'choose image'
            })
        }
# size create form


class SizeCreateForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = Size
        fields = ['name']

    # def clean_name(self):
    #     size = self.cleaned_data.get('name')
    #     if Size.objects.filter(name=size).exists():
    #         raise ValidationError('This Size already exists')

    #     return size


# customer create form

class CustomerCreateForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        
        def clean(self):
            cleaned_data = super().clean()
            username = self.cleaned_data['username']
            email = self.cleaned_data['email']
            mobile = self.cleaned_data['mobile']
            
            if Customer.objects.filter(username=username).exists():
                raise ValidationError({
                    'username': 'this username is not available'
                })
            if Customer.objects.filter(email=email).exists():
                raise ValidationError({
                    'email': 'user with this email already exists'
                })
            if Customer.objects.filter(mobile=mobile):
                raise ValidationError({
                    'mobile': 'user with this mobile no. already exists'
                })
            if len(mobile) < 10:
                raise ValidationError({
                    'mobile': 'Invalid mobile no.'
                })

# contact

class ContactForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

        def clean_email(self):
            email = self.cleaned_data['email']
            if '@' not in email:
                raise forms.ValidationError({
                    'email': 'Enter valid email'})
            return email


# service

class ServiceForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = service
        fields = '__all__'

        
# message
class MessageForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'

        def clean_email(self):
            email = self.cleaned_data['email']
            if '@' not in email:
                raise forms.ValidationError({
                    'email': 'Enter valid email'})
            return email