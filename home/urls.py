from django.urls import path
from .import views
from .views import *

app_name = 'home'

urlpatterns = [
    path('', HomeTemplateView.as_view(), name="home"),
    # products
    path('products/list/', ProductListView.as_view(), name='product-list'),
    path('products/<slug:slug>/detail/',
         ProductDetailView.as_view(), name='product-detail'),
    path('contact/', ContactView.as_view(), name="contact"),
]
