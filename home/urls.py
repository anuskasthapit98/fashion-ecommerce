from django.urls import path
from .import views
from .views import *

app_name = 'home'

urlpatterns = [
    path('', HomeTemplateView.as_view(), name="home"),
    
    #registration
    path('register/', CustomerRegistrationView.as_view(), name="register"),
    
    # products
    path('products/list/', ProductListView.as_view(), name='product-list'),
    path('products/<slug:slug>/detail/',
         ProductDetailView.as_view(), name='product-detail'),

     #contact    
    path('contact/', ContactView.as_view(), name="contact"),

    #Newsletter
    path('newsletter/', SubscriptionView.as_view(), name='newsletter'),

    #blogs 
    path('blogs/', BlogView.as_view(), name ='blogs'),
    path('blogs/<int:pk>/detail/', BlogDetailView.as_view(), name = 'blog-detail'),


]

