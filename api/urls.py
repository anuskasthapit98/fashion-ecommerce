from django.urls import path
from .views import *

app_name = 'api'
urlpatterns = [
    path('product/api/', ProductListCreate.as_view()),
    path('product/<slug:pk>/api/', ProductUpdateDelete.as_view()),
    path('category/', CategoryListCreate.as_view()),
    path('category/<int:pk>/', CategoryUpdateDelete.as_view()),
    path('brand/', BrandListCreate.as_view()),
    path('brand/<int:pk>/', BrandUpdateDelete.as_view()),
]
