from django.urls import path
from .import views
from .views import *

app_name = 'home'

urlpatterns = [
    path('', HomeTemplateView.as_view(), name="home"),

    # registration
    path('customer/register/', CustomerRegistrationView.as_view(), name="register"),
    path('customer/login/', CustomerLoginView.as_view(), name="login"),
    path('customer/logout/', CustomerLogoutView.as_view(), name="logout"),
    path('customer/forgot/password',
         CustomerForgotPasswordView.as_view(), name="forgot-password"),
    path('customer/change/password',
         CustomerPasswordsChangeView.as_view(), name="change-password"),

    path("profile/", CustomerProfileView.as_view(), name="customerprofile"),
    path("profile/order-<int:pk>/", CustomerOrderDetailView.as_view(),
         name="customerorderdetail"),


    # products
    path('products/list/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/detail/',
         ProductDetailView.as_view(), name='product-detail'),
    path('products/quick/view/', ProductQuickView.as_view(),
         name='product-quick-view'),

    # about
    path('abouts/', AboutListView.as_view(), name="abouts"),


    # contact
    path('contact/', ContactView.as_view(), name="contact"),

    # Newsletter
    path('newsletter/', SubscriptionView.as_view(), name='newsletter'),

    # blogs
    path('blogs/', BlogView.as_view(), name='blogs'),
    path('blogs/<int:pk>/detail/', BlogDetailView.as_view(), name='blog-detail'),

    # cart funtionality url
    path('add-to-cart/<int:pro_id>/', AddToCartView.as_view(), name='add-to-cart'),
    # my cart
    path('my-cart/', MyCartView.as_view(), name='my-cart'),
    #update-quantity
     path('update-quantity/', UpdateQuantityView.as_view(), name='update-quantity'),
    # manage cart
    path('manage/<int:p_id>cart/', ManageCartView.as_view(), name='manage-cart'),

    # checkout
    path('checkout/', CheckoutView.as_view(), name='checkout'),

    # coupon
    path('coupon/', CouponView.as_view(), name='coupon'),


    path('add-to-wishlist/<int:pro_id>/', WishlistView.as_view(), name='add-to-wishlist'),
    path('my-wishlist/', MyWishListView.as_view(), name='my-wishlist'),

]
