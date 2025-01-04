from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from apps.shapeteam.models import ExerciseRanking
from apps.shapeteam.serializers import ExerciseRankingSerializer


class ExerciseRankingAPIView(APIView):
    queryset = ExerciseRanking.objects.all()
    serializer_class = ExerciseRankingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # return self.queryset.objects.
        ...