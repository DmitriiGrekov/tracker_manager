from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from .models import Company
from users.models import User

from users.serializers import UserShortSerializer


class CompanySerializer(serializers.ModelSerializer):
    users = UserShortSerializer(read_only=True, many=True)
    author = UserShortSerializer(read_only=True)

    class Meta:
        model = Company
        fields = (
                'id',
                'name',
                'description',
                'image',
                'author',
                'users',
                )
        read_only_fields = ('author',)

    def create(self, validated_data):
        try:
            company = Company.objects.create(**validated_data)
            user = User.objects.get(pk=validated_data.get('author').pk)
            user.company = company
            user.save()
            return company
        except User.DoesNotExist:
            raise AuthenticationFailed('Not authenticated')
