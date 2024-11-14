from django.contrib.auth import get_user_model, login
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from knox.auth import TokenAuthentication
from knox.models import AuthToken
from rest_framework import status, exceptions
from rest_framework.generics import CreateAPIView, UpdateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from knox import views as knox_views
from .serializers import *
from .utils import Util


class RegisterAPIView(CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
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
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        response = super().post(request, *args, **kwargs)
        return response


class UpdateUserAPI(UpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UpdateUserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class ChangePasswordView(UpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = ChangePasswordSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
