from django.urls import path
from .views import *

from . import views

app_name = 'dashboard'
urlpatterns = [

    # path('login/', LoginView.as_view(), name="admin_login"),
    # path('logout/', LogoutView.as_view(), name="admin_logout"),
    # path('dashboard/', AdminDashboardView.as_view(),name="admin_dashboard"),
  
    # path('updatepassword/', PasswordsChangeView.as_view(), name="update_password"),
  
    # path('password-forgot/', ForgotPasswordView.as_view(), name= 'forgotpassword'),
    # path('password-reset/<int:pk>', PasswordResetView.as_view(), name= 'passwordreset'),
  
    

    # # users
    # path('user/create', UserCreateView.as_view(), name='user-create'),
    # path('user/list', UsersListView.as_view(), name="user_list"),
    
]