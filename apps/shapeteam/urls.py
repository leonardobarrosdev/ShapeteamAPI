from django.urls import path, re_path
from . import views
from .views.connection import TrainingPartnerAPIView

urlpatterns = [
    path('exercises/', views.ExercisesAPIView.as_view(), name='exercise-list'),
    path('exercises/<int:pk>/', views.ExerciseAPIView.as_view(), name='exercise-detail'),
    path('exerciserankings/', views.ExercisesRankingAPIView.as_view(), name='exerciseranking-list'),
    path('exerciserankings/<int:pk>/', views.ExerciseRankingAPIView.as_view(), name='exerciseranking-detail'),
    path('gyms/', views.GymsAPIView.as_view(), name='gym-list'),
    path('gyms/<int:pk>/', views.GymAPIView.as_view(), name='gym-detail'),
    path('muscle-groups/', views.MuscleGroupAPIView.as_view(),name='muscle-group'),
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
        r'^training-partners/(?P<pk>\d+)/accept_request/$',
        TrainingPartnerAPIView.as_view({'post': 'accept_request'}),
        name='training-partners-accept'
    ),
    re_path(
        r'^training-partners/(?P<pk>\d+)/reject_request/$',
        TrainingPartnerAPIView.as_view({'delete': 'reject_request'}),
        name='training-partners-reject'
    ),
    re_path(
        r'^training-partners/potential_partners/$',
        TrainingPartnerAPIView.as_view({'get': 'potential_partners'}),
        name='training-partners-potential'
    ),
]

