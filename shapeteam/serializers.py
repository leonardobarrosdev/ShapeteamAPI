from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'gender')


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {
            'password': {'required': True}
        }

    def validate(self, attrs):
        email = attrs.get('email', '').strip().lower()
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('User with this email id already exists.')
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'thumbnail', 'email', 'gender', 'password')

    def update(self, instance, validated_data):
        password = validated_data.pop('password')
        if password:
            instance.set_password(password)
        instance = super().update(instance, validated_data)
        return instance


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email').lower()
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError("Please give both email and password.")

        if not CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email does not exist.')

        user = authenticate(request=self.context.get('request'), email=email,
                            password=password)
        if not user:
            raise serializers.ValidationError("Wrong Credentials.")

        attrs['user'] = user
        return attrs


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
        fields = ['id', 'name_exe', 'name', 'description', 'default_reps', 'default_sets', 'muscle_group', 'photo']

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
        fields = (
            'routine',
            'weekday',
            'exercises'
        )


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
        fields = (
            'user',
            'exercise',
            'score',
            'update'
            )


class GymSerializer(serializers.ModelSerializer):

    class Meta:
        model = Gym
        fields = (
            'name',
            'location'
        )
        

class SearchSerializer(UserSerializer):
	status = serializers.SerializerMethodField()

	class Meta:
		model = CustomUser
		fields = [
			'username',
			'name',
			'thumbnail',
			'status'
		]
	
	def get_status(self, obj):
		if obj.pending_them:
			return 'pending-them'
		elif obj.pending_me:
			return 'pending-me'
		elif obj.connected:
			return 'connected'
		return 'no-connection'


class RequestSerializer(serializers.ModelSerializer):
	sender = UserSerializer()
	receiver = UserSerializer()

	class Meta:
		model = Connection
		fields = [
			'id',
			'sender',
			'receiver',
			'created'
		]


class FriendSerializer(serializers.ModelSerializer):
	friend = serializers.SerializerMethodField()
	preview = serializers.SerializerMethodField()
	updated = serializers.SerializerMethodField()
	
	class Meta:
		model = Connection
		fields = [
			'id',
			'friend',
			'preview',
			'updated'
		]

	def get_friend(self, obj):
		# If Im the sender
		if self.context['user'] == obj.sender:
			return UserSerializer(obj.receiver).data
		# If Im the receiver
		elif self.context['user'] == obj.receiver:
			return UserSerializer(obj.sender).data
		else:
			print('Error: No user found in friendserializer')

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


class ChatSerializer(serializers.ModelSerializer):
	# is_me = serializers.SerializerMethodField()

	class Meta:
		model = Chat
		fields = [
			'id',
			# 'is_me',
            'user',
			'text',
			'created'
		]

	def get_is_me(self, obj):
		return self.context['user'] == obj.user

