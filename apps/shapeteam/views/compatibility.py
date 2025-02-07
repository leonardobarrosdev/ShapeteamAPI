from knox.auth import TokenAuthentication
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.response import Response
from apps.shapeteam.models import Connection, UserPerformanceMetrics
from apps.user.models import Address
from apps.user.serializers import UserSerializer


class UserCompatibilityViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    
    def get_queryset(self):
        """
        This function defines the custom queryset for the UserCompatibilityViewSet;
        End users will be filtered and ordered by performance metrics.
        Return a list of users that match the criteria (completion rate of top to dow).
        """
        user = self.request.user
        existing_partners = Connection.objects.filter(
                Q(sender=user) | Q(receiver=user)
            ).values_list('sender', 'receiver')
        existing_partner_ids = set(
            [partner_id for partners in existing_partners for partner_id in partners]
        )
        users = self.queryset.exclude(id__in=existing_partner_ids).exclude(id=user.id)
        return users
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        # user = self.request.user
        # address = Address.objects.get(user=user)
        # if address:
        #     queryset = self.find_by_address(address)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def find_by_address(self, address):
        """Find users by address"""
        user = self.request.user
        queryset = self.get_queryset()
        addresses = Address.objects.exclude(user=user).filter(city=address.city)
        users = queryset.filter(id__in=addresses.values('user'))
        return users

    def find_by_features(self, features):
        """It filters users based on their IMC, age and level"""
        user = self.request.user
        queryset = self.get_queryset()
        imc, age, level = user.get_imc(), user.get_age(), user.level
        users = queryset.filter(
            Q(imc__gte=imc-1) | Q(imc__lte=imc+1) &
            Q(age__gte=age-1) | Q(age__lte=age+1) &
            Q(level=level)
        )
        return users
    
    @classmethod
    def find_by_performance(cls, users):
        """
        Find users by performance metrics
        order by completion rate
        return a list of users ordered by completion rate
        """
        performance_metrics = UserPerformanceMetrics.objects.filter(user__in=users)
        users = performance_metrics.order_by('completion_rate')
        return users
