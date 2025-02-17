from rest_framework import serializers
from apps.user.serializers import ProfileSerializer, UserSerializer
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


class WeekRoutineSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeekRoutine
        fields = ['id', 'user']

    def create(self, validated_data):
        return WeekRoutine.objects.create(**validated_data)


class DayTrainingSerializer(serializers.ModelSerializer):
    weekday = serializers.CharField(required=False)
    muscle_group = MuscleGroupSerializer(many=True)
    week_routine = WeekRoutineSerializer()

    class Meta:
        model = DayTraining
        fields = '__all__'

    def partial_update(self, instance, validated_data):
        return super().update(instance, validated_data)


class DayTrainingCreateSerializer(serializers.ModelSerializer):
    muscle_group = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=MuscleGroup.objects.all()
    )
    week_routine = serializers.PrimaryKeyRelatedField(
        queryset=WeekRoutine.objects.all()
    )

    class Meta:
        model = DayTraining
        exclude = ['id']

    def create(self, validated_data):
        muscle_groups = validated_data.pop('muscle_group', [])
        week_routine = validated_data.pop('week_routine')
        day_training = DayTraining.objects.create(**validated_data)
        for muscle_group in muscle_groups:
            day_training.muscle_group.add(muscle_group.id)
        day_training.week_routine = week_routine
        return day_training


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
    receiver = ProfileSerializer(read_only=True)
    
    class Meta:
        model = Connection
        fields = '__all__'
        read_only_fields = ('accepted',)


class ConnectionSenderSerializer(serializers.ModelSerializer):
    sender = ProfileSerializer(read_only=True)
    
    class Meta:
        model = Connection
        fields = '__all__'
        read_only_fields = ('accepted',)


class ConnectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = '__all__'
        read_only_fields = ('accepted',)