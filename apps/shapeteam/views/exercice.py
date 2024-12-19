from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from ..models import Exercise, ExerciseRanking
from ..serializers import (
    ExerciseSerializer,
    ExerciseRankingSerializer,
)


class ExercisesAPIView(generics.ListCreateAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    permissions = ['add_exercise', 'view_exercise']


class ExerciseAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    permissions = ['view_exercise', 'change_exercise', 'delete_exercise']


class ExercisesRankingAPIView(generics.ListCreateAPIView):
    queryset = ExerciseRanking.objects.all()
    serializer_class = ExerciseRankingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    permissions = ['add_exercise_ranking', 'view_exercise_ranking']


class ExerciseRankingAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ExerciseRanking.objects.all()
    serializer_class = ExerciseRankingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    permissions = [
        'view_exercise_ranking',
        'change_exercise_ranking',
        'delete_exercise_ranking'
    ]