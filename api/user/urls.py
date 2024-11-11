from django.urls import path
from knox.views import LogoutView, LogoutAllView
from . import views

app_name = 'user'

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout-all/', LogoutAllView.as_view(), name='logout'),
    path('update/<int:pk>/', views.UpdateUserAPI.as_view(), name='update'),
    path('change_password/<int:pk>/', views.ChangePasswordView.as_view(), name='change_password'),
    path('email-verify/', views.VerifyEmailAPIView.as_view(), name='email-verify')
]