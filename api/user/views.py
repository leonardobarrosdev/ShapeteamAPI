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
        # getting access tokens
        token = AuthToken.objects.create(user)[1]
        # send email for user verification
        current_site = get_current_site(request).domain
        relative_link = reverse('user:email-verify')
        protocol = 'http://' if DEBUG else 'https://'
        url = protocol + current_site + relative_link + "?token=" + str(token)
        email_body = _('Hi ') + user['last_name'] + \
                     _(' Use the link below to verify your email \n') + url
        data = {'email_body': email_body, 'to_email': user['email'],
                'email_subject': _('Verify your email')}
        Util.send_email(data=data)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token
        })


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
        try:
            user = AuthToken.objects.get(token_key=token[:8]).user
            if user.is_active:
                return Response({"message": _("Account already verified.")}, status=status.HTTP_400_BAD_REQUEST)
            user.is_active = True
            user.save()
            return Response({"message": _("Email successfully verified!")}, status=status.HTTP_200_OK)
        except AuthToken.DoesNotExist:
            return Response({"error": _("Invalid or expired token.")}, status=status.HTTP_400_BAD_REQUEST)