from users.models import User
from .serializers import ProjectSerializer
from .models import Project
from .exceptions import NoDataEmailsException

from company.models import Company


def get_project_user_auth(user: User) -> list[Project]:
    """Просмотр списка проектов авторизованного пользователя"""
    projects = user.projects.all()
    return projects


def get_project_company(company_id: int) -> list[Project]:
    """Просмотр всех проектов компании"""
    company = Company.objects.get(pk=company_id)
    projects = company.projects.all()
    return projects


def get_one_project(project_id: int, user_id: int) -> Project:
    """Получение одного проекта"""
    project = Project.objects.get(pk=project_id,
                                  users__id=user_id)
    return project


def create_project(validated_data, user: User) -> Project:
    """Создание проекта"""
    serializer = ProjectSerializer(data=validated_data)
    serializer.is_valid(raise_exception=True)
    project = serializer.save(users=[user],
                              company=user.company)
    return project


def update_project(project_id: int, user_id: int, validated_data) -> Project:
    """Обновление проекта"""
    project = get_one_project(project_id, user_id)
    serializer = ProjectSerializer(project,
                                   data=validated_data,
                                   partial=True)
    serializer.is_valid(raise_exception=True)
    project = serializer.save()
    return project


def delete_project(project_id: int, user_id: int):
    """Удаление проекта"""
    project = get_one_project(project_id, user_id)
    project.delete()
    return project


def update_user_in_project(users_email: list[str],
                           project_id: int, user: User) -> Project:
    """Обновление пользователей в проекте"""
    if not users_email:
        raise NoDataEmailsException('Не переданы почты пользователей')
    users = User.objects.filter(email__in=users_email)
    project = Project.objects.get(pk=project_id,
                                  users__id=user.id)
    project.users.set([*users, user])
    return project
