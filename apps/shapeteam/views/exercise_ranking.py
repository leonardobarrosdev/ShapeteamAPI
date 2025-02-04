from django.contrib.auth import get_user_model
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.shapeteam.models import ExerciseRanking
from apps.shapeteam.serializers import ExerciseRankingSerializer


class UserRankingAPIView(APIView):
    queryset = ExerciseRanking.objects.all()
    serializer_class = ExerciseRankingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_score_by_user_level(self, level):
        ranking = self.queryset.objects.filter(user_level=level).order_by('-score')
        return self.serializer_class(ranking).data