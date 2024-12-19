from knox.auth import TokenAuthentication
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.shapeteam.models import MuscleGroup
from apps.shapeteam.serializers import MuscleGroupSerializer


class MuscleGroupAPIView(generics.ListAPIView):
    queryset = MuscleGroup.objects.all()
    serializer_class = MuscleGroupSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
