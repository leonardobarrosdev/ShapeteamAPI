from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from knox.auth import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from apps.shapeteam.serializers import (
    ConnectionCreateSerializer,
    ConnectionSerializer,
    ConnectionSenderSerializer
)
from apps.shapeteam.models import Connection
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
import ipdb


User = get_user_model()

class TrainingPartnerAPIView(viewsets.ModelViewSet):
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    
    def list(self, request):
        """Get all connection requests for the current user"""
        users = Connection.objects.filter(
            Q(accepted=True) & (
                Q(sender=request.user) |
                Q(receiver=request.user)
            )
        )
        page = self.paginate_queryset(users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)
    
    def pending(self, request):
        """Get all connection requests for the current user"""
        users = Connection.objects.filter(accepted=False, receiver=request.user)
        serializer = ConnectionSenderSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """
        Create a new connection request
        Prevents duplicate requests and self-connections
        """
        receiver_id = request.data.get('receiver')
        if int(receiver_id) == request.user.id:
            return Response(
                {"error": _("You cannot send a connection request to yourself")},
                status=status.HTTP_400_BAD_REQUEST
            )
        existing_connection = Connection.objects.filter(
            Q(sender=request.user, receiver_id=receiver_id) |
            Q(receiver=request.user, sender_id=receiver_id)
        ).exists()
        if existing_connection:
            return Response(
                {"error": _("Connection request already exists")},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Create new connection request
        serializer = ConnectionCreateSerializer(data={
            'sender': request.user.id,
            'receiver': receiver_id
        })
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['POST'])
    def accept_request(self, request, pk=None):
        """Accept a connection request"""
        receiver = request.user
        try:
            sender = User.objects.get(id=pk)
            connection = Connection.objects.get(
                sender=sender.id,
                receiver=receiver.id,
                accepted=False
            )
            connection.accepted = True
            connection.save()
            serializer = ConnectionSenderSerializer(connection)
            return Response(serializer.data)
        except User.DoesNotExist or Connection.DoesNotExist:
            return Response(
                {"error": _("Connection request not found")},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['DELETE'])
    def reject_request(self, request, pk=None):
        """Reject or cancel a connection request"""
        receiver = request.user
        try:
            sender = User.objects.get(id=pk)
            connection = Connection.objects.get(sender=sender, receiver=receiver)
            connection.delete()
            return Response(
                {"message": _("Connection request deleted")},
                status=status.HTTP_204_NO_CONTENT
            )
        except Connection.DoesNotExist:
            return Response(
                {"error": _("Connection request not found")},
                status=status.HTTP_404_NOT_FOUND
            )
