from django.urls import path
from .views import *
from dashboard import views

app_name = 'dashboard'
urlpatterns = [
    path('dashboard/', AdminDashboardView.as_view(), name="admin-dashboard"),

     #authenticate
    path('login/', LoginView.as_view(), name="admin-login"),
    path('logout/', LogoutView.as_view(), name="admin-logout"),
    path('recoverpassword/', RecoverPasswordView.as_view(), name="recoverpassword"),
    path('changepassword/', PasswordsChangeView.as_view(), name="change-password"),
    
    # Category
    path('dashboard/category/', CategoryListView.as_view(), name="category"),
    path('dashboard/category/create/',
         CategoryCreateView.as_view(), name="category-create"),
    path('dashboard/category/<slug:slug>/update/',
         CategoryUpdateView.as_view(), name="category-update"),
    path('dashboard/category/<slug:slug>/delete/',
         CategoryDeleteView.as_view(), name="category-delete"),

     #category  API
     
     path('category/', views.CategoryListCreate.as_view()),
     path('category/<int:pk>/', views.CategoryUpdateDelete.as_view()),


     #products
    path('dashboard/product/image/create/',
         ProductImageCreateView.as_view(), name='product-image-create'),
    path('dashboard/product/create/',
         ProductCreateView.as_view(), name='product-create'),
    path('dashboard/product/<slug:slug>/update/',
         ProductUpdateView.as_view(), 'product-update'),
    path('dashboard/product/list/',
         ProductListView.as_view(), name='product-list'),
    path('dashboard/product/<slug:slug>/delete,',
         ProductDeleteView.as_view(), name='product-delete'),

     #brands
    path('dashboard/brand/list/', BrandListView.as_view(), name='brand-list'),
    path('dashboard/brand/create/', BrandCreateView.as_view(), name='brand-create'),
    path('dashboard/brand/<int:pk>/update/',
         BrandUpdateView.as_view(), name='brand-update'),
    path('dashboard/brand/<int:pk>/delete/',
         BrandDeleteView.as_view(), name='brand-delete'),
   
    
]
