from django.urls import path
from .views import *

app_name = 'dashboard'
urlpatterns = [
    path('dashboard/', AdminDashboardView.as_view(), name="admin- dashboard"),
    path('login/', LoginView.as_view(), name="admin_login"),
    path('logout/', LogoutView.as_view(), name="admin_logout"),
    path('recoverpassword/', RecoverPasswordView.as_view(), name= "recoverpassword"),
    path('changepassword/', PasswordsChangeView.as_view(), name="change_password"),
]
