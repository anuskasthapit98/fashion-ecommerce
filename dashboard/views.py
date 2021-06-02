from re import template
from dashboard.models import Category
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import *
# Create your views here.

class AdminDashboardView(TemplateView):
	template_name = 'dashboard/base/index.html'



class CategoryListView(ListView):
    Model = Category
    template_name = 'dashboard/Category/list.html'
    context_object_name = 'category'
    