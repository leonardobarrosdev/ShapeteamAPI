from datetime import datetime
from knox.auth import TokenAuthentication
from django.contrib.auth import get_user_model
from django.db.models import (
    Q, F, FloatField, IntegerField, ExpressionWrapper, DateField, Value
)
from django.db.models.functions import Round, ExtractDay
from rest_framework import viewsets, status
from rest_framework.response import Response
from apps.shapeteam.models import Connection
from apps.user.models import Address
from apps.user.serializers import UserSerializer
from apps.shapeteam.models import Gym


class UserCompatibilityViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.exclude(is_superuser=True)
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    
    def get_queryset(self):
        """
        This function defines the custom queryset for the UserCompatibilityViewSet;
        Filter users that are not already connected with the current user and exclude the current user;
        return the queryset.
        """
        user = self.request.user
        existing_partners = Connection.objects.filter(
                Q(sender=user) | Q(receiver=user)
            ).values_list('sender', 'receiver')
        existing_partner_ids = [partner_id for partners in existing_partners for partner_id in partners]
        users = self.queryset.exclude(id__in=existing_partner_ids).exclude(id=user.id)
        return users
    
    def list(self, request):
        user_address = self.find_by_address()
        user_features = self.find_by_features()
        queryset = user_address.filter(id__in=user_features)
        if not queryset:
            queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
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
        """
        It filters users based on their IMC, age, level and goal
        rerun users with similar feactures.
        """
        user = self.request.user
        queryset = self.get_queryset()
        imc, age, level, goals = user.get_imc(), user.get_age(), user.level, user.goal.all()
        # Anotate the queryset with the IMC for search user
        queryset = self.queryset.annotate(
            age=ExpressionWrapper(
                ExtractDay(
                    ExpressionWrapper(
                        Value(datetime.now()) - F('date_birth'),
                        output_field=DateField()
                    )
                )
                / 365.25,
                output_field=IntegerField()
            ),
            imc=Round(F('weight') / (F('height') ** 2.0), output_field=FloatField())
        )
        # Define the IMC range for filtering
        age_tolerance, imc_tolerance = 10, 5
        users = queryset.filter(
            Q(age__gte=age - age_tolerance, age__lte=age + age_tolerance) |
            Q(imc__gte=imc - imc_tolerance, imc__lte=imc + imc_tolerance) |
            Q(age=age) |
            Q(imc=imc) |
            Q(level=level) &
            Q(goal__in=goals)
        ).distinct()
        return users
    
    def find_by_gym(self):
        """Find users by gym location"""
        queryset = self.get_queryset()
        user_ids = Gym.objects.get(location__user=self.request.user).values('user')
        queryset = queryset.filter(id__in=user_ids)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
