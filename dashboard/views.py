from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy

from .forms import *
# Create your views here.


class DeleteMixin():
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class NonDeletedItemMixin():
    def get_qyeryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class AdminDashboardView(TemplateView):
    template_name = 'dashboard/base/index.html'


class ProductCreateView(CreateView):
    template_name = 'dashboard/product/create.html'
    form_class = ProductForm
    success_url = reverse_lazy('dashboard:product-list')


class PrductUpdateView(UpdateView):
    template_name = 'dashboard/product/create.html'
    model = Products
    form_class = ProductForm
    success_url = reverse_lazy('dashboard:product-list')


class ProductListView(NonDeletedItemMixin, ListView):
    template_name = 'dashboard/product/list.html'
    model = Products


class ProductDeleteView(DeleteMixin, DeleteView):
    model = Products
    success_url = reverse_lazy('dashboard:product-list')
