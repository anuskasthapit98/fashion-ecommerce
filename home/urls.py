from django.urls import path
from .import views
from .views import *

# app_name = 'home'

urlpatterns = [
    path('', HomeTemplateView.as_view(), name="home"),
    # path('', NewsletterView.as_view(), name="newsletter"),
    path('contact/', ContactView.as_view(), name="contact"),
]
