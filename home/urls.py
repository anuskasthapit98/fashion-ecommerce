from django.urls import path
from .import views
from .views import *

app_name = 'home'

urlpatterns = [
    path('', HomeTemplateView.as_view(), name="home"),
    # products
    path('products/list/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/detail/',
         ProductDetailView.as_view(), name='product-detail'),

    # about
    path('abouts/', AboutListView.as_view(), name="abouts"),


    # contact
    path('contact/', ContactView.as_view(), name="contact"),

    # Newsletter
    path('newsletter/', SubscriptionView.as_view(), name='newsletter'),

    # cart funtionality url
    path('add-to-cart/<int:pro_id>/', AddToCartView.as_view(), name='add-to-cart'),
    # my cart
    path('my-cart/', MyCartView.as_view(), name='my-cart'),
    # manage cart
    path('manage/<int:p_id>cart/', ManageCartView.as_view(), name='manage-cart'),

    # coupen validation
    path('coupen/validation/', CoupenValidation.as_view(),
         name='coupon-validation'),




]
