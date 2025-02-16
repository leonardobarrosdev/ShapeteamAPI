from django.urls import path, re_path
from . import views
from .views.connection import TrainingPartnerAPIView

urlpatterns = [
    path('exercises/', views.ExercisesAPIView.as_view(), name='exercise-list'),
    path('exercises/<int:pk>/', views.ExerciseAPIView.as_view(), name='exercise-detail'),
    path('exerciserankings/', views.ExercisesRankingAPIView.as_view(), name='exerciseranking-list'),
    path('gyms/', views.GymsAPIView.as_view(), name='gym-list'),
    path('gyms/<int:pk>/', views.GymAPIView.as_view(), name='gym-detail'),
    path('muscle-groups/', views.MuscleGroupsAPIView.as_view(), name='muscle-group-list'),
    path('week-routines/', views.WeekRoutinesAPIView.as_view(), name='week-routine-list'),
    path('week-routines/<int:pk>/', views.WeekRoutineAPIView.as_view(), name='week-routine-detail'),
    path('day-trainings/', views.DayTrainingsAPIView.as_view(), name='day-training-list'),
    path('day-training/', views.DayTrainingCreateAPIView.as_view(), name='day-training-create'),
    path('day-trainings/<int:pk>/', views.DayTrainingAPIView.as_view(), name='day-training-detail'),
    path(
        'day-trainings/<str:weekday>/',
         views.DaytrainingByWeekdayAPIView.as_view(),
         name='day-training-detail'
    ),
    re_path(
        'explore/',
        views.UserCompatibilityViewSet.as_view({'get': 'list'}),
        name='user-compatibility'
    ),
    re_path(
        r'^training-partners/$',
        TrainingPartnerAPIView.as_view({'get': 'list'}),
        name='training-partners-list'
    ),
    re_path(
        r'^training-partners/create/$',
        TrainingPartnerAPIView.as_view({'post': 'create'}),
        name='training-partners-create'
    ),
    re_path(
        r'^training-partners-pending/$',
        TrainingPartnerAPIView.as_view({'get': 'pending'}),
        name='training-partners-pending'
    ),
    re_path(
        r'^training-partners/(?P<pk>\d+)/accept_request/$',
        TrainingPartnerAPIView.as_view({'post': 'accept_request'}),
        name='training-partners-accept'
    ),
    re_path(
        r'^training-partners/(?P<pk>\d+)/reject_request/$',
        TrainingPartnerAPIView.as_view({'delete': 'reject_request'}),
        name='training-partners-reject'
    )
]

