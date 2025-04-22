from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

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

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def find_by_muscle_group(self, request, **kwargs):
        try:
            exercises = Exercise.objects.filter(
                muscle_group__in=request.data['muscle_group']
            )
            serializer = self.get_serializer(data=exercises)
            return Response(serializer.data, status=HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_406_NOT_ACCEPTABLE
            )


class ExerciseAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    permissions = ['view_exercise', 'change_exercise', 'delete_exercise']


class ExercisesRankingAPIView(generics.ListAPIView):
    queryset = ExerciseRanking.objects.all()
    serializer_class = ExerciseRankingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    permissions = ['add_exercise_ranking', 'view_exercise_ranking']
