from django.urls import path
from .views import *

app_name = 'api'
urlpatterns = [
    # product api
    path('product/api/', ProductListCreate.as_view()),
    # path('product/<slug:pk>/api/', ProductUpdateDelete.as_view()),

    
    # coupon api
    path('coupon/', CouponListCreate.as_view()),
    path('coupon/<int:pk>/', CouponUpdateDelete.as_view()),
    # path('product/<slug:pk>/api/', ProductUpdateDelete.as_view()),

    # category api
    path('category/', CategoryListCreate.as_view()),
    path('category/<int:pk>/', CategoryUpdateDelete.as_view()),

    # brand api
    path('brand/', BrandListCreate.as_view()),
    path('brand/<int:pk>/', BrandUpdateDelete.as_view()),

    # size api
    path('size/', SizeListCreate.as_view()),
    path('size/<int:pk>/', SizeUpdateDelete.as_view()),
]
