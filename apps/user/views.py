from django.contrib.auth import get_user_model, login
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
import ipdb
from knox.auth import TokenAuthentication
from knox.models import AuthToken
from rest_framework import status, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser
from knox import views as knox_views
from .serializers import *
from .utils import Util


User = get_user_model()

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return True # To not perform the csrf check


class RegisterAPIView(CreateAPIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    queryset = get_user_model().objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': 'Invalid fields.'}, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save()
        token_object, token = AuthToken.objects.create(user)
        email_body = render_to_string('emails/welcome.txt', {'user': user})
        data = {
            'email_subject': _('Welcome to Shapeteam - Your Ultimate Fitness Partner!'),
            'email_body': _(email_body),
            'to_email': user.email
        }
        Util.send_email(data=data)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token
        }, status=status.HTTP_201_CREATED)


class LoginAPIView(knox_views.LoginView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        response = super().post(request, *args, **kwargs)
        user_serializer = ProfileSerializer(user)
        response.data['user'] = user_serializer.data
        return response


class UpdateUserAPIView(UpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UpdateUserSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, JSONParser)

    def update(self, request, *args, **kwargs):
        try:
            user = request.user
            serializer = self.get_serializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                    "user": serializer.data,
                    "detail": _("Successfully updated.")
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'detail': _("Isn't possible to update user: ") + str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class ChangePasswordAPIView(UpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        serializer.update(user, serializer.validated_data)
        return Response(
            {"detail": _("Password successfully changed.")},
            status=status.HTTP_200_OK
        )


class SearchUserAPIView(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        """Search users by first name or last name"""
        search = self.request.query_params.get('search', None)
        if search is None:
            return User.objects.none()
        return User.objects.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search)
        )