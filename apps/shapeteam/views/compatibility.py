from knox.auth import TokenAuthentication
from django.contrib.auth import get_user_model
from django.db.models import Q, Avg, F, FloatField, ExpressionWrapper
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
        existing_partner_ids = [partner_id for partners in existing_partners for partner_id in partners]
        users = self.queryset.exclude(id__in=existing_partner_ids).exclude(id=user.id)
        return users
    
    def list(self, request):
        # address = self.find_by_address()
        # features = self.find_by_features()
        # users = address.objects.contains(id__in=features.values('id'))
        users = self.find_by_address()
        queryset = self.get_queryset() if not users else users
        # usr = self.find_by_performance(queryset)
        # if usr:
        #     queryset = usr
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def find_by_address(self):
        """Find users by address"""
        user = self.request.user
        try:
            address = Address.objects.get(user=user)
            addresses = Address.objects.exclude(user=user).filter(city=address.city)
            queryset = self.get_queryset()
            users = queryset.filter(id__in=addresses.values('user'))
            return users
        except Address.DoesNotExist:
            return None

    def find_by_features(self):
        """It filters users based on their IMC, age and level"""
        user = self.request.user
        queryset = self.get_queryset()
        imc, age, level = user.get_imc(), user.get_age(), user.level
        # Calculate median IMC and age
        # median_imc = queryset.aggregate(
        #     median_imc=Avg(ExpressionWrapper(F('weight') / (F('height') ** 2),
        #     output_field=FloatField()))
        # )['median_imc']
        # median_age = queryset.aggregate(median_age=Avg('date_birth'))['median_age']
        # users = queryset.filter(
        #     Q(imc__gte=median_imc-1) | Q(imc__lte=median_imc+1) &
        #     Q(age__gte=median_age-1) | Q(age__lte=median_age+1)
        # )
        users = queryset.filter(level=level)
        return users
    
    @classmethod
    def find_by_performance(cls, users):
        """
        Find users by performance metrics
        order by completion rate
        return a list of users ordered by completion rate
        """
        performance_metrics = UserPerformanceMetrics.objects.filter(user__id__in=users)
        users = performance_metrics.order_by('completion_rate')
        return users
