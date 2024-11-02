from django.urls import path
from knox.views import LogoutView, LogoutAllView
from . import views

urlpatterns = [
    path('nameexercise/', views.NameExerciseAPIView.as_view(),name='nameexercise-list'),

    #Exercises
    path('exercises/', views.ExercisesAPIView.as_view(),name='exercise-list'),
    path('exercises/<int:pk>/', views.ExerciseAPIView.as_view(),name='exercise-detail'),

    #ExerciseRanking
    path('exerciserankings/', views.ExercisesRankingAPIView.as_view(),name='exerciseranking-list'),
    path('exerciserankings/<int:pk>/', views.ExerciseRankingsAPIView.as_view(),name='exerciseranking-detail'),

    #DayExercise
    path('dayexercises/', views.DayExercisesAPIView.as_view(),name='dayexercise-list'),
    path('dayexercises/<int:pk>/', views.DayExerciseAPIView.as_view(),name='dayexercise-detail'),

    #Messages
    path('messages/', views.ChatsAPIView.as_view(),name='chat-list'),
    path('messages/<int:pk>/', views.ChatAPIView.as_view(),name='chat-detail'),

    #Gyms
    path('gyms/', views.GymsAPIView.as_view(),name='gym-list'),
    path('gyms/<int:pk>/', views.GymAPIView.as_view(),name='gym-detail'),
    
    #User
    path('create-user/', views.CreateUserAPI.as_view(), name='create-user'),
    path('update-user/<int:pk>/', views.UpdateUserAPI.as_view(), name='update-user'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout-all/', LogoutAllView.as_view(), name='logout-all'),
]

