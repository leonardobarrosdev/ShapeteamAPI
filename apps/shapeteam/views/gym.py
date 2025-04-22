from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from ..models import Gym
from ..serializers import GymSerializer


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