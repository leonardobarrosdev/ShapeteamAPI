from django.urls import path, re_path
from knox.views import LogoutView, LogoutAllView
from . import views

app_name = 'user'

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout-all/', LogoutAllView.as_view(), name='logouts'),
    path('<int:pk>/update/', views.UpdateUserAPIView.as_view(), name='update'),
    path('<int:pk>/change-password/', views.ChangePasswordAPIView.as_view(), name='change-password'),
    re_path(r'^search-users/?$', views.SearchUserAPIView.as_view({'get': 'list'}), name='search-users'),
]