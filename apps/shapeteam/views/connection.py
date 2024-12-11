from django.contrib.auth import get_user_model
from knox.auth import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from apps.shapeteam.serializers import ConnectionSerializer
from apps.shapeteam.models import Connection
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from apps.user.serializers import UserSerializer

User = get_user_model()

class TrainingPartnerAPIView(viewsets.ModelViewSet):
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        """
        Retrieve connection requests for the current user
        Supports filtering by status and search
        """
        user = self.request.user
        status_filter = self.request.query_params.get('status')
        search = self.request.query_params.get('search', '')
        queryset = Connection.objects.filter(
            Q(sender=user) | Q(receiver=user)
        )
        if status_filter == 'pending':
            queryset = queryset.filter(accepted=False)
        elif status_filter == 'accepted':
            queryset = queryset.filter(accepted=True)
        if search:
            queryset = queryset.filter(
                Q(sender__first_name__icontains=search) |
                Q(sender__last_name__icontains=search) |
                Q(receiver__first_name__icontains=search) |
                Q(receiver__last_name__icontains=search)
            )
        return queryset

    def create(self, request, *args, **kwargs):
        """
        Create a new connection request
        Prevents duplicate requests and self-connections
        """
        receiver_id = request.data.get('receiver')
        if int(receiver_id) == request.user.id:
            return Response(
                {"error": "You cannot send a connection request to yourself"},
                status=status.HTTP_400_BAD_REQUEST
            )
        existing_connection = Connection.objects.filter(
            Q(sender=request.user, receiver_id=receiver_id) |
            Q(receiver=request.user, sender_id=receiver_id)
        ).exists()
        if existing_connection:
            return Response(
                {"error": "Connection request already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Create new connection request
        serializer = self.get_serializer(data={
            'sender': request.user.id,
            'receiver': receiver_id
        })
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['POST'])
    def accept_request(self, request, pk=None):
        """Accept a connection request"""
        connection = self.get_object()
        if connection.receiver != request.user:
            return Response(
                {"error": "You are not authorized to accept this request"},
                status=status.HTTP_403_FORBIDDEN
            )
        connection.accepted = True
        connection.save()
        serializer = self.get_serializer(connection)
        return Response(serializer.data)

    @action(detail=True, methods=['DELETE'])
    def reject_request(self, request, pk=None):
        """Reject or cancel a connection request"""
        connection = self.get_object()
        # Ensure the current user is either sender or receiver
        if connection.sender != request.user and connection.receiver != request.user:
            return Response(
                {"error": "You are not authorized to modify this request"},
                status=status.HTTP_403_FORBIDDEN
            )
        connection.delete()
        return Response(
            {"message": "Connection request deleted"},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=False, methods=['GET'])
    def potential_partners(self, request):
        """
        Find potential training partners based on search criteria
        Excludes existing connections and the current user
        """
        search = request.query_params.get('search', '')
        existing_partners = Connection.objects.filter(
            Q(sender=request.user) | Q(receiver=request.user)
        ).values_list('sender_id', 'receiver_id')
        # Flatten and remove duplicates
        existing_partner_ids = set(
            [partner_id for pair in existing_partners for partner_id in pair]
        )
        existing_partner_ids.add(request.user.id)
        # Find potential partners
        potential_partners = User.objects.exclude(id__in=existing_partner_ids).filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search)
        )
        serializer = UserSerializer(potential_partners, many=True)
        return Response(serializer.data)