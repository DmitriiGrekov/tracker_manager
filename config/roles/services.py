from .models import Role
from .exceptions import NoPermissionInRequest
from .serializers import RoleSerializer
from users.models import User
from permissions.models import Permission


def get_roles(user: User) -> list[Role]:
    """Вывод списка ролей по компании"""
    return user.company.roles.all()


def create_role(validated_data, user: User) -> Role:
    """Создание ролей компании"""
    permissions = _get_permission_from_request(validated_data.get('permissions')) # получаем права из запроса
    serializer = RoleSerializer(data=validated_data)
    serializer.is_valid(raise_exception=True)
    role = serializer.save(company=user.company)
    role.permissions.set(permissions)
    role.save()
    return role


def get_one_role(role_id: int, user: User) -> Role:
    """Просмотр одной роли"""
    return Role.objects.get(pk=role_id,
                            company=user.company)


def update_role(validated_data, role_id: int, user: User) -> Role:
    """Обновление роли"""
    role = Role.objects.get(pk=role_id,
                            company=user.company)
    permissions = _get_permission_from_request(validated_data.get('permissions'))
    serializer = RoleSerializer(role,
                                data=validated_data,
                                partial=True)
    serializer.is_valid(raise_exception=True)
    role = serializer.save(permissions=permissions)
    return role


def delete_role(role_id: int, user: User) -> Role:
    """Удаление роли"""
    role = Role.objects.get(pk=role_id,
                            company=user.company)
    role.delete()
    return Role


def _get_permission_from_request(permisisons_str: str) -> list[Permission]:
    """Получаем права из запроса"""
    if not permisisons_str:
        raise NoPermissionInRequest('Не переданы права в запросе')
    permissions_list = list(map(int, permisisons_str.split(', ')))
    permissions = Permission.objects.filter(pk__in=permissions_list)
    return permissions
