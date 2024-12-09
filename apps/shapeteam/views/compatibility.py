from knox.auth import TokenAuthentication
from django.contrib.auth import get_user_model
from django.db.models import Q, QuerySet
from rest_framework import generics, viewsets
from rest_framework.filters import BaseFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from apps.shapeteam.models import WeekRoutine, DayTraining
from apps.user.serializers import SearchSerializer
# from geopy.distance import geodesic

User = get_user_model()

class SmallResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


class FindPartnerAPIView(generics.GenericAPIView):
    queryset = get_user_model().objects.exclude(is_superuser=True)
    serializer_class = SearchSerializer
    pagination_class = SmallResultsSetPagination
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        assert self.queryset is not None, (
            "'%s' should either include a `queryset` attribute, "
            "or override the `get_queryset()` method."
            % self.__class__.__name__
        )
        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()
        return queryset

class WeekRoutineCompatibilityViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user = self.request.user
        week_routine = DayTraining.objects.filter(routime=user)

# Example 1: Basic Location-Based Filtering
class UserCompatibilityViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        # Find users within a specific radius
        current_user = self.request.user
        max_distance = 50  # kilometers

        return User.objects.filter(
            Q(location__distance_lte=(current_user.location, max_distance)) &
            Q(profile__age_range=current_user.profile.age_range)
        )


# Example 2: Multi-Criteria Compatibility Matching
class AdvancedCompatibilityViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        current_user = self.request.user

        return User.objects.filter(
            Q(location__city=current_user.location.city) &
            Q(profile__activities__overlap=current_user.profile.activities) &
            Q(profile__fitness_level__range=(
                current_user.profile.fitness_level - 1,
                current_user.profile.fitness_level + 1
            ))
        )


# Example 3: Custom Distance Calculation Filter
'''
class GeographicCompatibilityViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        current_user = self.request.user

        def compatible_users():
            all_users = User.objects.all()
            compatible = []

            for user in all_users:
                distance = geodesic(
                    (current_user.location.latitude, current_user.location.longitude),
                    (user.location.latitude, user.location.longitude)
                ).kilometers

                if distance <= 50 and self.is_compatible(current_user, user):
                    compatible.append(user.id)

            return User.objects.filter(id__in=compatible)

        return compatible_users()

    def is_compatible(self, user1, user2):
        # Custom compatibility logic
        return (
                abs(user1.profile.age - user2.profile.age) <= 5 and
                set(user1.profile.activities).intersection(user2.profile.activities)
        )
'''

# Example 4: Activity and Physical Condition Matching
class ActivityBasedCompatibilityViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        current_user = self.request.user

        return User.objects.filter(
            Q(profile__primary_sport__in=current_user.profile.preferred_sports) &
            Q(profile__fitness_condition__gte=current_user.profile.fitness_condition - 1) &
            Q(profile__fitness_condition__lte=current_user.profile.fitness_condition + 1)
        )


# Example 5: Weighted Compatibility Scoring
class WeightedCompatibilityViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        current_user = self.request.user

        # Custom queryset with annotated compatibility score
        return User.objects.annotate(
            compatibility_score=self.calculate_compatibility(current_user)
        ).filter(compatibility_score__gte=0.7)  # Only users with 70%+ compatibility

    def calculate_compatibility(self, current_user):
        from django.db.models import F, Value
        from django.db.models.functions import Coalesce

        return (
            Coalesce(
                (0.4 * self.location_score(current_user)) +
                (0.3 * self.activity_score(current_user)) +
                (0.3 * self.physical_condition_score(current_user)),
                Value(0)
            )
        )

    def location_score(self, current_user):
        # Implementation of location compatibility scoring
        ...

    def activity_score(self, current_user):
        # Implementation of activity compatibility scoring
        ...

    def physical_condition_score(self, current_user):
        # Implementation of physical condition compatibility scoring
        ...