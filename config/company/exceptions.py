class NoUserDataInRequest(Exception):
    pass


class NotFoundEmailData(Exception):
    """Ошибка отсутсивя почт пользователей в запросе"""
