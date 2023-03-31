from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from users.auth import JWTAuthentication

from .models import Project
from .serializers import ProjectSerializer
from .exceptions import NoDataEmailsException

from users.decorators import permit_if_role_in
from .services import (get_project_user_auth,
                       create_project,
                       get_one_project,
                       update_project,
                       delete_project,
                       update_user_in_project
                       )


class ProjectAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProjectSerializer
    authentication_classes = (JWTAuthentication,)

    @permit_if_role_in(['pravo-na-prosmotr-proektov'])
    def get(self, request):
        """Просмотр списка проектов авторизованного пользователя"""
        projects = get_project_user_auth(request.user)
        serializer = self.serializer_class(projects, many=True)
        return Response({'data': serializer.data,
                         'count': len(serializer.data)},
                        status=status.HTTP_200_OK)

    @permit_if_role_in(['pravo-na-sozdanie-proektov'])
    def post(self, request):
        """Добавление проекта"""
        project = create_project(request.data, request.user)
        serializer = self.serializer_class(project)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED)


class DetailUpdateDeleteAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProjectSerializer
    authentication_classes = (JWTAuthentication,)

    @permit_if_role_in(['pravo-na-prosmotr-proektov'])
    def get(self, request, project_id):
        try:
            project = get_one_project(project_id, request.user.id)
            serializer = self.serializer_class(project)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({'status': 404, 'message': 'Not Found'},
                            status=status.HTTP_404_NOT_FOUND)

    @permit_if_role_in(['pravo-na-obnovlenie-proektov'])
    def patch(self, request, project_id):
        """Обновление проекта"""
        try:
            project = update_project(project_id,
                                     request.user.id,
                                     request.data
                                     )
            serializer = ProjectSerializer(project)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({'status': 404, 'message': 'Not Found'},
                            status=status.HTTP_404_NOT_FOUND)

    @permit_if_role_in(['pravo-na-udalenie-proektov'])
    def delete(self, request, project_id):
        """Удаление проекта"""
        try:
            delete_project(project_id, request.user.id)
            return Response({'status': 200, 'message': 'Successfullly delete'},
                            status=status.HTTP_204_NO_CONTENT)
        except Project.DoesNotExist:
            return Response({'status': 404, 'message': 'Not Found'},
                            status=status.HTTP_404_NOT_FOUND)


class UpdateUserInProject(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProjectSerializer
    authentication_classes = (JWTAuthentication,)

    @permit_if_role_in(['pravo-na-obnovlenie-proektov'])
    def post(self, request, project_id):
        """Обновление пользователей в проекте"""
        try:
            project = update_user_in_project(request.data.get('users_email'),
                                             project_id,
                                             request.user)
            serializer = self.serializer_class(project)
            return Response(serializer.data,
                            status=status.HTTP_200_OK)

        except Project.DoesNotExist:
            return Response({'status': 404, 'message': 'Not Found'},
                            status=status.HTTP_404_NOT_FOUND)
        except NoDataEmailsException as e:
            return Response({'status': 400, 'message': e.__str__()},
                            status=status.HTTP_400_BAD_REQUEST)
