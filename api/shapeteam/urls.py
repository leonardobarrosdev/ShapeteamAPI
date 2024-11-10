from django.urls import path
from . import views

urlpatterns = [
    path('nameexercise/', views.NameExerciseAPIView.as_view(), name='nameexercise-list'),

    #Exercises
    path('exercises/', views.ExercisesAPIView.as_view(), name='exercise-list'),
    path('exercises/<int:pk>/', views.ExerciseAPIView.as_view(), name='exercise-detail'),

    #ExerciseRanking
    path('exerciserankings/', views.ExercisesRankingAPIView.as_view(), name='exerciseranking-list'),
    path('exerciserankings/<int:pk>/', views.ExerciseRankingAPIView.as_view(), name='exerciseranking-detail'),

    #DayExercise
    path('dayexercises/', views.DayExercisesAPIView.as_view(), name='dayexercise-list'),
    path('dayexercises/<int:pk>/', views.DayExerciseAPIView.as_view(), name='dayexercise-detail'),

    #Gyms
    path('gyms/', views.GymsAPIView.as_view(), name='gym-list'),
    path('gyms/<int:pk>/', views.GymAPIView.as_view(), name='gym-detail'),
]

