from django.contrib.auth import get_user_model, login, logout
from rest_framework import generics, status
from rest_framework import generics
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from knox import views as knox_views
from django.contrib.auth import login
from .models import *
from .serializers import *


class CreateUserAPI(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)


class UpdateUserAPI(UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UpdateUserSerializer
    permission_classes = (IsAuthenticated,)


class LoginAPIView(knox_views.LoginView):
    permission_classes = (AllowAny, )
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            login(request, user)
            response = super().post(request, format=None)
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response(response.data, status=status.HTTP_200_OK)


class ExercisesAPIView(generics.ListCreateAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permissions = ['add_exercise', 'view_exercise']
     

class ExerciseAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permissions = ['change_exercise', 'delete_exercise']


class NameExerciseAPIView(generics.ListCreateAPIView):
    queryset = NameExercise.objects.all()
    serializer_class = NameExerciseSerializer
    permission_classes = [IsAuthenticated]
    permissions = ['add_name_exercise', 'view_name_exercise']


class DayExercisesAPIView(generics.ListCreateAPIView):
    queryset = DayExercise.objects.all()
    serializer_class = DayExerciceSerializer
    permissions = ['add_day_exercise', 'view_day_exercise']


class DayExerciseAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DayExercise.objects.all()
    serializer_class = DayExerciceSerializer
    permissions = ['change_day_exercise', 'delete_day_exercise']
   
    
class ChatsAPIView(generics.ListCreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    # authentication_classes = [AllowAny]
    permissions = ['add_chat', 'view_chat']


class ChatAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    # authentication_classes = [IsAuthenticated]
    permissions = ['change_chat', 'delete_chat']


class ExercisesRankingAPIView(generics.ListCreateAPIView):
    queryset = ExerciseRanking.objects.all()
    serializer_class = ExerciseRankingSerializer
    permissions = ['add_exercise_ranking', 'view_exercise_ranking']


class ExerciseRankingsAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ExerciseRanking.objects.all()
    serializer_class = ExerciseRankingSerializer
    permissions = ['change_exercise_ranking', 'delete_exercise_ranking']


class GymsAPIView(generics.ListCreateAPIView):
    queryset = Gym.objects.all()
    serializer_class = GymSerializer
    permissions = ['add_gym', 'view_gym']


class GymAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Gym.objects.all()
    serializer_class = GymSerializer
    permissions = ['change_gym', 'delete_gym']
