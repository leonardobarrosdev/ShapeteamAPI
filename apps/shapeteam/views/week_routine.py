from knox.auth import TokenAuthentication
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.shapeteam.models import WeekRoutine
from apps.shapeteam.serializers import WeekRoutineSerializer


class WeekRoutinesAPIView(generics.ListAPIView):
    queryset = WeekRoutine.objects.all()
    serializer_class = WeekRoutineSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return WeekRoutine.objects.filter(
            user=self.request.user
        ).values('days_training__weekday', 'days_training__muscle_group')


class WeekRoutineAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WeekRoutine.objects.all()
    serializer_class = WeekRoutineSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return WeekRoutine.objects.filter(
            user=self.request.user
        ).values('day_training')