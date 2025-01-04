from knox.auth import TokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from apps.shapeteam.models import MuscleGroup
from apps.shapeteam.serializers import MuscleGroupSerializer


class MuscleGroupsAPIView(ListAPIView):
    queryset = MuscleGroup.objects.all()
    serializer_class = MuscleGroupSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return MuscleGroup.objects.filter(user=self.request.user)
