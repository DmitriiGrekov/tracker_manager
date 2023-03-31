from .models import Permission


def get_permissions() -> list[Permission]:
    """Получение списка прав"""
    return Permission.objects.all()
