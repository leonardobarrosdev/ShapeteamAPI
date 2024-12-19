from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import CustomUser, Address


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'first_name', 'email', 'gender')


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password', 'password2']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        email = attrs.get('email', '').strip().lower()
        password = attrs.get('password')
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError(_('User with this email id already exists.'))
        if password != attrs.get('password2'):
            raise serializers.ValidationError(_('Invalid password.'))
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)

    class Meta:
        model = CustomUser
        fields = [
            'username', 'first_name', 'last_name', 'thumbnail', 'email', 'gender', 'weight', 'date_birth', 'level', 'goal'
        ]

    def validate_email(self, value):
        user = self.context['request'].user
        if CustomUser.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({"email": _("This email is already in use.")})
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if user.id != instance.id:
            raise serializers.ValidationError({"authorize": _("You dont have permission for this user.")})
        instance = super().update(instance, validated_data)
        return instance


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email').lower()
        password = attrs.get('password')
        if not email or not password:
            raise serializers.ValidationError(_("Please give both email and password."))
        if not CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError(_('Email does not exist.'))
        user = authenticate(request=self.context.get('request'), email=email, password=password)
        if not user:
            raise serializers.ValidationError(_("Wrong Credentials."))
        attrs['user'] = user
        return attrs


class SearchSerializer(UserSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'thumbnail', 'status']

    def get_status(self, obj):
        if obj.pending_them:
            return 'pending-them'
        elif obj.pending_me:
            return 'pending-me'
        elif obj.connected:
            return 'connected'
        return 'no-connection'


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        help_text=_("New password. Must meet password complexity requirements.")
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        help_text=_("Confirm new password by repeating it.")
    )
    old_password = serializers.CharField(
        write_only=True,
        required=True,
        help_text=_("Current password for verification.")
    )

    class Meta:
        model = CustomUser
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": _("Password fields didn't match.")})
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": _("Old password is not correct")})
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = CustomUser
        fields = ['token']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
