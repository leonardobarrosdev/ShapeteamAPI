from knox.auth import TokenAuthentication
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import *


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


class NameExerciseAPIView(generics.ListCreateAPIView):
    queryset = NameExercise.objects.all()
    serializer_class = NameExerciseSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    permissions = ['add_name_exercise', 'view_name_exercise']


class DayExercisesAPIView(generics.ListCreateAPIView):
    queryset = DayExercise.objects.all()
    serializer_class = DayExerciceSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    permissions = ['add_day_exercise', 'view_day_exercise']


class DayExerciseAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DayExercise.objects.all()
    serializer_class = DayExerciceSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    permissions = [
        'view_day_exercise',
        'change_day_exercise',
        'delete_day_exercise'
    ]


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


class GymsAPIView(generics.ListCreateAPIView):
    queryset = Gym.objects.all()
    serializer_class = GymSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    permissions = ['add_gym', 'view_gym']


class GymAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Gym.objects.all()
    serializer_class = GymSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    permissions = ['view_gym', 'change_gym', 'delete_gym']
