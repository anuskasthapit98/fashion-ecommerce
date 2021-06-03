from django.urls import path
from .views import *

app_name = 'dashboard'
urlpatterns = [
    path('dashboard/', AdminDashboardView.as_view(), name="admin-dashboard"),
    
    
    #Category
    path('category/', CategoryListView.as_view(), name = "category"),
    path('category/create/', CategoryCreateView.as_view(), name = "category_create"),
    # path('category/update/<int:pk>/', CategoryListView.as_view(), name = "category_update"),
    # path('category/delete/<int:pk>/', CategoryListView.as_view(), name = "category_delete"),
]
