from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, response
from django.views.generic import ListView, TemplateView, DetailView, CreateView



from dashboard.models import *
# Create your views here.
class HomeTemplateView(TemplateView):
    template_name = 'home/base/index.html'
    
    def get_context_data(self, **kwargs) :
       context = super().get_context_data(**kwargs)
       context['blogs'] = Blog.objects.filter(deleted_at__isnull=True)
       
       return context