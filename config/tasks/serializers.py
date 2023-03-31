from rest_framework import serializers
from .models import Task, TaskFiles

from users.serializers import UserShortSerializer
from projects.serializers import ProjectSerializer
from company.serializers import CompanySerializer


class TaskFileSerializer(serializers.ModelSerializer):
    """Сериализатор файлов к задачам"""

    class Meta:
        model = TaskFiles
        fields = ('file', 'task',)


class TaskSerializer(serializers.ModelSerializer):
    """Сериализатор задач"""
    author = UserShortSerializer(read_only=True)
    executor = UserShortSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)
    company = CompanySerializer(read_only=True)

    class Meta:
        model = Task
        fields = ('id',
                  'name',
                  'description',
                  'author',
                  'executor',
                  'project',
                  'company',
                  'date_sprint',
                  'status',
                  'time_tracker',
                  'created_at',
                  'updated_at')
