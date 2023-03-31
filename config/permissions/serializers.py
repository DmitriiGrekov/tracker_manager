from rest_framework import serializers
from .models import Permission


class PermissionSerializer(serializers.ModelSerializer):
    """Сериализер прав"""

    class Meta:
        model = Permission
        fields = ('id', 'name', 'slug',)
