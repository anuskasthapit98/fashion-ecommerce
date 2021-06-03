from re import template

from django.db.models.base import Model
from dashboard.models import Category
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView
from .forms import *
from .models import Category
from django.urls import reverse_lazy
# Create your views here.

class AdminDashboardView(TemplateView):
	template_name = 'dashboard/base/index.html'



class CategoryListView(ListView):
    template_name = 'dashboard/Category/list.html'

    
    def get_queryset(self):
        return Category.objects.filter(parent__isnull=True)
    
class CategoryCreateView(CreateView):
    template_name = 'dashboard/Category/form.html'
    Model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('dashboard:category')
    

    
    
    