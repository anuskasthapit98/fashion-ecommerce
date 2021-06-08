
from django.conf import settings as conf_settings
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import TemplateView, FormView, View, CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.http import JsonResponse


from .models import *
from .mixin import *
from .forms import *

# Create your views here.
# login view starts here


class LoginView(FormView):
    template_name = 'dashboard/auth/login.html'
    form_class = StaffLoginForm
    success_url = reverse_lazy('dashboard:admin-dashboard')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        pword = form.cleaned_data['password']
        user = authenticate(username=username, password=pword)

        if user is not None:
            login(self.request, user)
            user.is_active = True

        else:
            return render(self.request, self.template_name,
                          {
                              'error': 'Invalid Username or password',
                              'form': form
                          })

        return super().form_valid(form)


# logout view
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/login/')


# password reset view
class RecoverPasswordView(FormView):
    template_name = 'dashboard/auth/recover-password.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('dashboard:admin_login')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        user = User.objects.filter(email=email).first()
        password = get_random_string(8)
        user.set_password(password)
        user.save(update_fields=['password'])

        text_content = 'Your password has been changed. {} '.format(password)
        send_mail(
            'Password Reset | Sleek',
            text_content,
            conf_settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        messages.success(self.request, "Password reset code is sent")
        return super().form_valid(form)


# password change view
class PasswordsChangeView(PasswordChangeView):
    template_name = 'dashboard/auth/password_change.html'
    form_class = ChangePasswordForm
    success_url = reverse_lazy('dashboard:admin_login')

    def get_form(self):
        form = super().get_form()
        form.set_user(self.request.user)
        return form


# dashboard views
class AdminDashboardView(AdminRequiredMixin, TemplateView):
    template_name = 'dashboard/base/index.html'


class AdminDashboardView(TemplateView):
    template_name = 'dashboard/base/index.html'


# category's view starts here
class CategoryListView(NonDeletedItemMixin, ListView):
    template_name = 'dashboard/Category/list.html'
    model = Category

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(parent__isnull=True)
        return queryset


class CategoryCreateView(CreateView):
    template_name = 'dashboard/Category/form.html'
    form_class = CategoryForm
    success_url = reverse_lazy('dashboard:category')


class CategoryUpdateView(UpdateView):
    template_name = 'dashboard/Category/form.html'
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('dashboard:category')


class CategoryDeleteView(DeleteMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('dashboard:category')


# Product

class ProductImageCreateView(CreateView):
    model = ProductImage
    form_class = ProductImageForm
    template_name = "dashboard/product/imageform.html"

    def dispatch(self, request, *args, **kwargs):
        if self.request.is_ajax():
            return super().dispatch(request, *args, **kwargs)
        return JsonResponse({"error": "Cannot access this page"}, status=404)

    def form_valid(self, form):
        instance = form.save()
        return JsonResponse(
            {
                "status": "ok",
                "pk": instance.pk,
                "url": instance.image.url,
            }
        )

    def form_invalid(self, form):
        return JsonResponse({"errors": form.errors}, status=400)


# products view starts here
class ProductListView(NonDeletedItemMixin, ListView):
    template_name = 'dashboard/product/list.html'
    model = Products


class ProductCreateView(CreateView):
    template_name = 'dashboard/product/create.html'
    form_class = ProductForm
    success_url = reverse_lazy('dashboard:product-list')


class ProductUpdateView(UpdateView):
    template_name = 'dashboard/product/create.html'
    model = Products
    form_class = ProductForm
    success_url = reverse_lazy('dashboard:product-list')


class ProductDeleteView(DeleteMixin, DeleteView):
    model = Products
    success_url = reverse_lazy('dashboard:product-list')
    template_name = 'dashboard/base/index.html'


# brand's views starts here


class BrandListView(NonDeletedItemMixin, ListView):
    template_name = 'dashboard/brand/list.html'
    model = Brands


class BrandCreateView(CreateView):
    template_name = 'dashboard/brand/create.html'
    form_class = BrandForm
    success_url = reverse_lazy('dashboard:brand-list')


class BrandUpdateView(UpdateView):
    template_name = 'dashboard/brand/create.html'
    model = Brands
    form_class = BrandForm
    success_url = reverse_lazy('dashboard:brand-list')


class BrandDeleteView(DeleteMixin, DeleteView):
    model = Brands
    success_url = reverse_lazy('dashboard:brand-list')
