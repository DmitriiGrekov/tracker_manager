from rest_framework import serializers
from permissions.serializers import PermissionSerializer
from .models import Role


class RoleSerializer(serializers.ModelSerializer):
    """Сериализер ролей"""
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Role
        fields = ('id', 'name', 'slug', 'company', 'permissions',)
        read_only_fields = ('slug', 'company',)
