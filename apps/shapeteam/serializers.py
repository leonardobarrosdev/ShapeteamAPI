from rest_framework import serializers
from apps.user.serializers import UserSerializer
from .models import *


class MuscleGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MuscleGroup
        fields = '__all__'


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = '__all__'

    def get_muscle_group(self, obj):
        return obj.muscle_group.name if obj.muscle_group else None

    def get_photo(self, obj):
        if obj.muscle_group.photo:
            return obj.muscle_group.photo.url
        return None


class DayTrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayTraining
        fields = '__all__'


class ExerciseRankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseRanking
        exclude = ('updated_at',)


class GymSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gym
        fields = ('name', 'location')


class RequestSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    receiver = UserSerializer()

    class Meta:
        model = Connection
        fields = ('id', 'sender', 'receiver', 'created_at')


class ConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = '__all__'
        read_only_fields = ('accepted',)


class WeekRoutineSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeekRoutine
        fields = '__all__'
