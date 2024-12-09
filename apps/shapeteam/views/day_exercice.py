from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from ..models import DayExercise
from ..serializers import DayExerciceSerializer


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