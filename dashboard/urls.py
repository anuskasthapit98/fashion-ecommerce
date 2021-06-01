
from django.urls import path, include
from .views import *

urlpatterns = [
   
    path('', AdminDashboardView.as_view(), name='dashboard'),
    
]
