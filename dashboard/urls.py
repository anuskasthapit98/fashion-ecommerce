from django.urls import path
from .views import *

app_name = 'dashboard'
urlpatterns = [

    # login
    path('login/', LoginView.as_view(), name="login"),
    # logout
    path('logout/', LogoutView.as_view(), name="logout"),
    # password reset
    path('recoverpassword/', RecoverPasswordView.as_view(), name="recover-password"),
    # password change
    path('changepassword/', PasswordsChangeView.as_view(), name="change-password"),

    # user list
    path('user/create', UserCreateView.as_view(), name='user-create'),
    path('user/list', UsersListView.as_view(), name="user-list"),
    path('userdisable/<int:pk>/',
         UserToggleStatusView.as_view(), name='user-disable'),
    # dashboard view
    path('dashboard/', AdminDashboardView.as_view(), name="dashboard"),

    # Category
    path('dashboard/category/', CategoryListView.as_view(), name="category"),
    path('dashboard/category/create/',
         CategoryCreateView.as_view(), name="category-create"),
    path('dashboard/category/<slug:slug>/update/',
         CategoryUpdateView.as_view(), name="category-update"),
    path('dashboard/category/<slug:slug>/delete/',
         CategoryDeleteView.as_view(), name="category-delete"),

    # image create
    path('dashboard/product/image/create/',
         ProductImageCreateView.as_view(), name='product-image-create'),

    # product urls here
    path('dashboard/product/list/',
         ProductListView.as_view(), name='product-list'),
    path('dashboard/product/create/',
         ProductCreateView.as_view(), name='product-create'),
    path('dashboard/product/<slug:slug>/update/',
         ProductUpdateView.as_view(), name='product-update'),

    path('dashboard/product/<slug:slug>/delete,',
         ProductDeleteView.as_view(), name='product-delete'),

    # brand urls
    path('dashboard/brand/list/', BrandListView.as_view(), name='brand-list'),
    path('dashboard/brand/create/', BrandCreateView.as_view(), name='brand-create'),
    path('dashboard/brand/<int:pk>/update/',
         BrandUpdateView.as_view(), name='brand-update'),
    path('dashboard/brand/<int:pk>/delete/',
         BrandDeleteView.as_view(), name='brand-delete'),


    # size urls
    path('dashboard/size/list/', SizeListView.as_view(), name='size-list'),
    path('dashboard/size/create/', SizeCreateView.as_view(), name='size-create'),
    path('dashboard/size/<int:pk>/update/',
         SizeUpdateView.as_view(), name='size-update'),
    path('dashboard/size/<int:pk>/delete/',
         SizeDeleteView.as_view(), name='size-delete'),


]
