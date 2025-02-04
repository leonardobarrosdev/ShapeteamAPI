from knox.auth import TokenAuthentication
from django.contrib.auth import get_user_model
from django.db.models import Q, QuerySet
from rest_framework import generics, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.shapeteam.models import WeekRoutine, DayTraining, UserPerformanceMetrics
from apps.user.models import Address
from apps.user.serializers import UserSerializer, SearchSerializer


User = get_user_model()

class WeekRoutineCompatibilityViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user = self.request.user
        week_routine = DayTraining.objects.filter(
            routine=WeekRoutine.user
        )


class UserCompatibilityViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_queryset(self):
        """
        This function defines the custom queryset for the UserCompatibilityViewSet.
        It filters users based on their IMC, age, level and location.
        End users will be filtered and ordered by performance metrics.
        Return a list of users that match the criteria (completion rate of top to dow).
        """
        user = self.request.user
        imc, age, level = user.get_imc(), user.get_age(), user.level
        address = Address.objects.get(user=user)
        address_list = Address.objects.filter(city=address.city)
        users = [ads.user for ads in address_list]
        for usr in users:
            if (imc - usr.get_imc() > 10) and (age - usr.get_age() > 10) or level != usr.level:
                users.remove(usr)
        users.remove(user)
        user_refs = UserPerformanceMetrics.objects.filter(user__in=users).order_by('-completion_rate').values('user')
        users = User.objects.filter(id__in=user_refs)
        return users
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
