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
        It filters users based on their IMC, age, level and location;
        End users will be filtered and ordered by performance metrics.
        Return a list of users that match the criteria (completion rate of top to dow).
        """
        user = self.request.user
        imc, age, level = user.get_imc(), user.get_age(), user.level
        address = Address.objects.get(user=user)
        address_list = Address.objects.filter(city=address.city)
        users = [ads.user for ads in address_list]
        existing_partners = Connection.objects.filter(
                Q(sender=user) | Q(receiver=user)
            ).values_list('sender', 'receiver')
        existing_partner_ids = set(
            [partner_id for partners in existing_partners for partner_id in partners]
        )
        for usr in users:
            if (imc - usr.get_imc() > 10) and (age - usr.get_age() > 10) or level != usr.level:
                users.remove(usr)
        user_refs = UserPerformanceMetrics.objects.exclude(user__in=existing_partner_ids).filter(user__in=users).order_by('-completion_rate').values('user')
        users = self.queryset.filter(id__in=user_refs)
        return users if users else self.queryset.exclude(user__in=existing_partner_ids)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
