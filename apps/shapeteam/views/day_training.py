from django.db.models import Q
from knox.auth import TokenAuthentication
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND

from apps.shapeteam.models import DayTraining
from apps.shapeteam.serializers import DayTrainingSerializer, DayTrainingCreateSerializer


class DayTrainingsAPIView(generics.ListCreateAPIView):
    queryset = DayTraining.objects.all()
    serializer_class = DayTrainingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return DayTraining.objects.filter(week_routine__user=self.request.user)


class DayTrainingCreateAPIView(generics.CreateAPIView):
    serializer_class = DayTrainingCreateSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args):
        serializer = DayTrainingCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class DayTrainingAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DayTraining.objects.all()
    serializer_class = DayTrainingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return DayTraining.objects.filter(week_routine__user=self.request.user)

    def get(self, request, *args, **kwargs):
        weekday = request.GET['weekday']
        if weekday:
            try:
                day_training = DayTraining.objects.filter(
                    Q(weekday=weekday) &
                    Q(week_routine__user=request.user)
                ).first()
                serializer = self.get_serializer(day_training)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except AttributeError:
                return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Bad request'}, status=HTTP_404_NOT_FOUND)

    def patch(self, request, *args, **kwargs):
        day_training = DayTraining.objects.get(id=kwargs['pk'])
        serializer = DayTrainingCreateSerializer(day_training, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        instance = DayTraining.objects.get(id=kwargs['pk'])
        serializer = DayTrainingCreateSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save(**serializer.validated_data)
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.error, status.HTTP_400_BAD_REQUEST)


class DaytrainingByWeekdayAPIView(generics.DestroyAPIView):
    queryset = DayTraining.objects.all()
    serializer_class = DayTrainingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        day_training = DayTraining.objects.filter(week_routine__user=self.request.user)
        return self.get_serializer(day_training).data

    def delete(self, request, *args, **kwargs):
        try:
            day_training = DayTraining.objects.filter(weekday=kwargs['weekday']).last()
            day_training.delete()
            return Response({'message': 'Deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except DayTraining.DoesNotExist:
            return Response({'error': 'Day training not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)