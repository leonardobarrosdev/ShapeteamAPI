from django.urls import path
from knox.views import LogoutView, LogoutAllView
from . import views

app_name = 'user'

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout-all/', LogoutAllView.as_view(), name='logouts'),
    path('<int:pk>/update/', views.UpdateUserAPI.as_view(), name='update'),
    path('<int:pk>/change-password/', views.ChangePasswordView.as_view(), name='change-password'),
]