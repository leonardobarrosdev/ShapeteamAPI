from django.contrib.auth import get_user_model, login
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from knox.models import AuthToken
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from knox import views as knox_views
from core.settings import DEBUG
from .serializers import *
from .utils import Util


User = get_user_model()

class RegisterAPIView(CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # Create a Knox token
        token_object, token = AuthToken.objects.create(user)
        token_key = token[:8]
        # send email for user verification
        current_site = get_current_site(request).domain
        relative_link = reverse('user:email-verify')
        protocol = 'http://' if DEBUG else 'https://'
        url = f"{protocol}{current_site}{relative_link}?token={token_key}:{token}"
        email_body = f'Hi {user.first_name},\nUse the link below to verify your email:\n{url}'
        data = {
            'email_subject': 'Verify your email',
            'email_body': email_body,
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
    permission_classes = (IsAuthenticated,)


class ChangePasswordView(UpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)


class VerifyEmailAPIView(GenericAPIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        token = request.GET.get('token')
        if not token or ':' not in token:
            return Response({"error": _("Invalid token format.")}, status=status.HTTP_400_BAD_REQUEST)
        token_key, token_digest = token.split(':', 1)
        try:
            auth_token = AuthToken.objects.authenticate(token_key, token_digest)
            if auth_token is None:
                raise AuthToken.DoesNotExist
            user = auth_token.user
            if user.is_active:
                return Response({"message": _("Account already verified.")}, status=status.HTTP_400_BAD_REQUEST)
            user.is_active = True
            user.save()
            return Response({"message": _("Email successfully verified!")}, status=status.HTTP_200_OK)
        except AuthToken.DoesNotExist:
            return Response({"error": _("Invalid or expired token.")}, status=status.HTTP_400_BAD_REQUEST)
