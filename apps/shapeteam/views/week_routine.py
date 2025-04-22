from knox.auth import TokenAuthentication
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.shapeteam.models import WeekRoutine
from apps.shapeteam.serializers import WeekRoutineSerializer


class WeekRoutinesAPIView(generics.ListCreateAPIView):
    queryset = WeekRoutine.objects.all()
    serializer_class = WeekRoutineSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return WeekRoutine.objects.filter(
            user=self.request.user
        ).values('days_training__weekday', 'days_training__muscle_group')

    def post(self, request, *args):
        data = {'user': self.request.user.id}
        serializer = WeekRoutineSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WeekRoutineAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WeekRoutine.objects.all()
    serializer_class = WeekRoutineSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return WeekRoutine.objects.filter(
            user=self.request.user
        ).values('day_training')