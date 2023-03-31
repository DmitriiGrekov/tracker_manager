from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User
from roles.serializers import RoleSerializer


class RegistrationSerializer(serializers.ModelSerializer):
    """Регистрация пользователя"""
    password = serializers.CharField(
            max_length=128,
            min_length=8,
            write_only=True
            )

    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'token']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    """Авторизация пользователя"""
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        """Аутентификация пользователя"""
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError('An email address is required to log in')

        if password is None:
            raise serializers.ValidationError('An password address is required to log in')

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError('A user with this email and password was not found')

        if not user.is_active:
            raise serializers.ValidationError('This user has been deactivated.')

        return {
                'email': user.email,
                'username': user.get_username(),
                'token': user.token
                }


class UserSerializer(serializers.ModelSerializer):
    """Обновление и вывод пользователя"""

    roles = RoleSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ('id',
                  'email',
                  'username',
                  'about',
                  'first_name',
                  'last_name',
                  'image',
                  'roles',
                  )
        read_only_fields = ('token',)


class UserShortSerializer(serializers.ModelSerializer):
    """Сериализатор без ненужных данных"""

    class Meta:
        model = User
        fields = ('id',
                  'username',
                  'about',
                  'first_name',
                  'last_name',
                  'image',
                  )
