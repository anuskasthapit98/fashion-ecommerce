from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

class AdminDashboardView(TemplateView):
	template_name = 'dashboard/base/index.html'
