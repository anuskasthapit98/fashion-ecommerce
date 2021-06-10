
from django.conf import settings as conf_settings
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.utils.crypto import get_random_string
from django.views.generic import TemplateView, FormView, View, CreateView, UpdateView, DeleteView, ListView

from .forms import *
from .models import *
from .mixin import *

# Create your views here.
# login view starts here


class LoginView(FormView):
    template_name = 'dashboard/auth/login.html'
    form_class = StaffLoginForm
    success_url = reverse_lazy('dashboard:dashboard')

    # def form_valid(self, form):
    #     username = form.cleaned_data['username']
    #     pword = form.cleaned_data['password']
    #     user = authenticate(username=username, password=pword)

    #     if user is not None:
    #         login(self.request, user)
    #         user.is_active = True

    #     else:
    #         return render(self.request, self.template_name,
    #                       {
    #                           'error': 'Invalid Username or password',
    #                           'form': form
    #                       })

    #     return super().form_valid(form)


# logout view
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/login/')


# password reset view
class RecoverPasswordView(FormView):
    template_name = 'dashboard/auth/recover-password.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('dashboard:login')

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
    success_url = reverse_lazy('dashboard:login')

    def get_form(self):
        form = super().get_form()
        form.set_user(self.request.user)
        return form

# user


class UserCreateView(SuperAdminRequiredMixin, AdminRequiredMixin, CreateView):
    template_name = 'dashboard/users/usercreate.html'
    form_class = UserForm
    success_url = reverse_lazy('dashboard:user-list')

    def get_success_url(self):
        return reverse('dashboard:recover-password', kwargs={'pk': self.object.pk})


class UsersListView(SuperAdminRequiredMixin, AdminRequiredMixin, ListView):
    template_name = 'dashboard/users/userlist.html'
    model = Account
    success_url = reverse_lazy('dashboard:user-list')
    paginate_by = 5


class UserToggleStatusView(View):
    success_url = reverse_lazy('dashboard:user-list')

    def get(self, request, *args, **kwargs):
        account = User.objects.filter(pk=self.kwargs.get("pk")).first()
        if account.is_active == True:
            account.is_active = False
        else:
            account.is_active = True
        account.save(update_fields=['is_active'])

        return redirect(self.success_url)

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
        if "name" in self.request.GET:
            if self.request.GET.get('name') != '':
                queryset = queryset.filter(
                    name=self.request.GET.get("name"))
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

    def get_queryset(self):
        queryset = super().get_queryset()
        if "name" in self.request.GET:
            if self.request.GET.get('name') != '':
                queryset = queryset.filter(
                    name__contains=self.request.GET.get("name"))
        if "brands" in self.request.GET:
            if self.request.GET.get('brands') != '':
                queryset = queryset.filter(
                    brands__name__contains=self.request.GET.get("brands"))
        if "categories" in self.request.GET:
            if self.request.GET.get('categories') != '':
                queryset = queryset.filter(
                    categories__name__contains=self.request.GET.get("categories"))
        return queryset


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

    def get_queryset(self):
        queryset = super().get_queryset()
        if "name" in self.request.GET:
            if self.request.GET.get('name') != '':
                queryset = queryset.filter(
                    name__contains=self.request.GET.get("name"))
        return queryset


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


# size view starts here


class SizeListView(NonDeletedItemMixin, ListView):
    template_name = 'dashboard/size/list.html'
    model = Size


class SizeCreateView(CreateView):
    template_name = 'dashboard/size/form.html'
    form_class = SizeCreateForm
    success_url = reverse_lazy('dashboard:size-list')


class SizeUpdateView(UpdateView):
    template_name = 'dashboard/size/form.html'
    model = Size
    form_class = SizeCreateForm
    success_url = reverse_lazy('dashboard:size-list')


class SizeDeleteView(DeleteMixin, DeleteView):
    model = Size
    success_url = reverse_lazy('dashboard:size-list')



# customer view starts here

class CustomerListView(NonDeletedItemMixin, ListView):
    template_name = 'dashboard/customer/list.html'
    model = Customer

    def get_queryset(self):
        queryset = super().get_queryset()
        if "username" in self.request.GET:
            if self.request.GET.get('username') != '':
                queryset = queryset.filter(
                    username__contains=self.request.GET.get("username"))
        return queryset


class CustomerCreateView(CreateView):
    template_name = 'dashboard/customer/create.html'
    form_class = CustomerCreateForm
    success_url = reverse_lazy('dashboard:customer-list')


class CustomerUpdateView(UpdateView):
    template_name = 'dashboard/customer/create.html'
    model = Customer
    form_class = CustomerCreateForm
    success_url = reverse_lazy('dashboard:customer-list')


class CustomerDeleteView(DeleteMixin, DeleteView):
    model = Customer
    success_url = reverse_lazy('dashboard:customer-list')