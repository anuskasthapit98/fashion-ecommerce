from django.urls import path
from .views import *

app_name = 'dashboard'
urlpatterns = [
    path('dashboard/', AdminDashboardView.as_view(), name="admin-dashboard"),
    path('dashboard/product/image/create/',
         ProductImageCreateView.as_view(), name='product-image-create'),
    path('dashboard/product/create/',
         ProductCreateView.as_view(), name='product-create'),
    path('dashboard/product/<slug:slug>/update/',
         PrductUpdateView.as_view(), 'product-update'),
    path('dashboard/product/list/',
         ProductListView.as_view(), name='product-list'),
    path('dashboard/product/<slug:slug>/delete,',
         ProductDeleteView.as_view(), name='product-delete'),

    path('dashboard/', AdminDashboardView.as_view(), name="admin- dashboard"),
    path('login/', LoginView.as_view(), name="admin_login"),
    path('logout/', LogoutView.as_view(), name="admin_logout"),
    path('recoverpassword/', RecoverPasswordView.as_view(), name="recoverpassword"),
    path('changepassword/', PasswordsChangeView.as_view(), name="change_password"),
]
