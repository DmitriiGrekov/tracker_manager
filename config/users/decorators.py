from functools import wraps
from rest_framework import status
from rest_framework.response import Response


def permit_if_role_in(allowed_permissions=()):
    """Данный декоратор проверяет наличие прав у пользователя"""

    def view_wrapper_function(decorated_view_function):
        """ This intermediate wrapper function takes the decorated View function (e.g. get, post) itself. """
        @wraps(decorated_view_function)
        def enforce_user_permissions(view, request, *args, **kwargs):
            """ A function that intercepts the View function and enforces permissions """
            for role in request.user.roles.all():
                if role.permissions.filter(slug=allowed_permissions[0]):
                    response = decorated_view_function(view,
                                                       request,
                                                       *args,
                                                       **kwargs)
                    return response
            return Response({'status': 403, 'message': 'No permissions'},
                            status=status.HTTP_403_FORBIDDEN)
        return enforce_user_permissions
    return view_wrapper_function
