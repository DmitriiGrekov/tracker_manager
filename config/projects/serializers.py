from rest_framework import serializers
from .models import Project
from users.serializers import UserShortSerializer
from company.serializers import CompanySerializer


class ProjectSerializer(serializers.ModelSerializer):
    """Сериалайзер проектов"""

    users = UserShortSerializer(many=True, read_only=True)
    company = CompanySerializer(read_only=True)

    class Meta:
        model = Project
        fields = ('id',
                  'name',
                  'description',
                  'users',
                  'company',
                  'is_active',
                  'created_at'
                  )
