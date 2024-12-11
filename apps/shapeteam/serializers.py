from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from apps.user.serializers import UserSerializer
from .models import *


class NameExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = NameExercise
        fields = '__all__'


class ExerciseSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    muscle_group = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()

    class Meta:
        model = Exercise
        fields = (
            'id',
            'name_exe',
            'name',
            'description',
            'default_reps',
            'default_sets',
            'muscle_group',
            'photo'
        )

    def get_description(self, obj):
        return obj.name_exe.description if obj.name_exe else None

    def get_name(self, obj):
        return obj.name_exe.name if obj.name_exe else None

    def get_muscle_group(self, obj):
        return obj.name_exe.muscle_group if obj.name_exe else None

    def get_photo(self, obj):
        return obj.name_exe.photo.url if obj.name_exe and obj.name_exe.photo else None


class DayTrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayTraining
        fields = ('routine', 'weekday', 'exercises')


class DayExerciceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayExercise
        fields = (
            'user',
            'exercise',
            'reps',
            'sets',
            'duration'
        )


class ExerciseRankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseRanking
        fields = ('user', 'exercise', 'score', 'update')


class GymSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=120, required=True)

    class Meta:
        model = Gym
        fields = ('name', 'location')


class RequestSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    receiver = UserSerializer()

    class Meta:
        model = Connection
        fields = ('id', 'sender', 'receiver', 'created')


class FriendSerializer(serializers.ModelSerializer):
	friend = serializers.SerializerMethodField()
	preview = serializers.SerializerMethodField()
	updated = serializers.SerializerMethodField()
	
	class Meta:
		model = Connection
		fields = ('id', 'friend', 'preview', 'updated')

	def get_friend(self, obj):
		if self.context['user'] == obj.sender:
			return UserSerializer(obj.receiver).data
		elif self.context['user'] == obj.receiver:
			return UserSerializer(obj.sender).data
		else:
			raise _('Error: No user found in friendserializer')

	def get_preview(self, obj):
		default = 'New connection'
		if not hasattr(obj, 'latest_text'):
			return default
		return obj.latest_text or default

	def get_updated(self, obj):
		if not hasattr(obj, 'latest_created'):
			date = obj.updated
		else:
			date = obj.latest_created or obj.updated
		return date.isoformat()


class ConnectionSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()
    receiver_name = serializers.SerializerMethodField()

    class Meta:
        model = Connection
        fields = ['id', 'sender', 'receiver', 'accepted', 'created', 'updated',
                  'sender_name', 'receiver_name']
        read_only_fields = ['accepted']

    def get_sender_name(self, obj):
        return obj.sender.get_full_name() or obj.sender.username

    def get_receiver_name(self, obj):
        return obj.receiver.get_full_name() or obj.receiver.username
