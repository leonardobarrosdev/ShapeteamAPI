from knox.auth import TokenAuthentication
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.shapeteam.models import DayTraining
from apps.shapeteam.serializers import DayTrainingSerializer


class DayTrainingsAPIView(generics.ListCreateAPIView):
    queryset = DayTraining.objects.all()
    serializer_class = DayTrainingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return DayTraining.objects.filter(user=self.request.user)


class DayTrainingAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DayTraining.objects.all()
    serializer_class = DayTrainingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return DayTraining.objects.filter(user=self.request.user)