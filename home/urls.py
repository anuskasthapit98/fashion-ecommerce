from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .views import *

app_name = 'home'
urlpatterns = [
    path('api/product/', ProductApiView.as_view(),
         name='api-product-list'),
    path('api/product/<int:id>/id', ProductApiIdview.as_view()),

]
