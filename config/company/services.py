from users.models import User
from permissions.models import Permission
from roles.models import Role
from .models import Company
from .serializers import CompanySerializer
from .exceptions import NotFoundEmailData


def get_user_company(user: User) -> list[Company]:
    """Получение компаний в которых учавствует пользователь"""
    companies = user.companies.all()
    return companies


def get_company_list() -> list[Company]:
    """Получение списка компаний"""
    companies = Company.objects.all()
    return companies


def create_company(validated_data, user: User) -> Company:
    """Создание компании"""
    serializer = CompanySerializer(data=validated_data)
    serializer.is_valid(raise_exception=True)
    company = serializer.save(author=user)
    permissions = Permission.objects.all()
    role = Role.create_need_role('Создатель компании',
                                 company,
                                 permissions)
    user.roles.add(role)
    return company


def update_company(validated_data, company_id: int, user: User) -> Company:
    """Обновление компании"""
    company = Company.objects.get(pk=company_id,
                                  users__id=user.pk)
    serializer = CompanySerializer(company,
                                   data=validated_data,
                                   partial=True)
    serializer.is_valid(raise_exception=True)
    company = serializer.save()
    return company


def delete_company(company_id: int, user: User) -> Company:
    """Удаление компании создателем"""
    company = Company.objects.get(pk=company_id,
                                  author__id=user.pk)
    company.delete()
    return Company


def add_user_in_company(user: User, users_email) -> Company:
    """Добавление людей в компанию"""
    company = user.company
    if not users_email:
        # return Response({'status': 400, 'message': 'No data emails'},
        #                 status=status.HTTP_400_BAD_REQUEST)
        raise NotFoundEmailData('Не переданы почты пользователей')
    users = User.objects.filter(email__in=users_email)
    for user in users:
        user.company = company
        user.save()
    return company


def delete_user_from_company(user: User, users_email) -> Company:
    """Удаление людей из компании"""
    company = user.company
    if not users_email:
        # return Response({'status': 400, 'message': 'No data emails'},
        #                 status=status.HTTP_400_BAD_REQUEST)
        raise NotFoundEmailData('Не переданы почты пользователей')
    users = User.objects.filter(email__in=users_email,
                                company=company)
    for user in users:
        user.company = None
        user.roles.clear()
        user.save()
    return company
