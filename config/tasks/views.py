from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from users.auth import JWTAuthentication
from users.decorators import permit_if_role_in
from users.models import User
from projects.models import Project

from .serializers import TaskSerializer
from .models import Task
from .services import (get_all_task_project,
                       create_task,
                       get_task_user,
                       get_one_task,
                       update_task,
                       delete_task,
                       track_task
                       )


class TaskAPIView(APIView):
    """Получение списка задач по проекту и создание задачи в проекте"""
    permission_classes = (IsAuthenticated,)
    serializer_class = TaskSerializer
    authentication_classes = (JWTAuthentication,)

    @permit_if_role_in(['pravo-na-prosmotr-zadach'])
    def get(self, request, project_id):
        """Получение задач проекта"""
        try:
            tasks = get_all_task_project(project_id,
                                         request.user)
            serializer = self.serializer_class(tasks,
                                               many=True)
            return Response({'data': serializer.data,
                             'count': len(serializer.data)},
                            status=status.HTTP_200_OK)
        except Project.DoesNotExist as e:
            return Response({'status': 404, 'message': e.__str__()},
                            status=status.HTTP_404_NOT_FOUND)

    @permit_if_role_in(['pravo-na-sozdanie-zadach'])
    def post(self, request, project_id):
        """Создание задачи в проекте"""
        try:
            task = create_task(request.data,
                               project_id,
                               request.user)
            serializer = self.serializer_class(task)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        except Project.DoesNotExist as e:
            return Response({'status': 404, 'message': e.__str__()},
                            status=status.HTTP_404_NOT_FOUND)


class TaskUserAPIView(APIView):
    """Получение списка задач пользователя"""
    permission_classes = (IsAuthenticated,)
    serializer_class = TaskSerializer
    authentication_classes = (JWTAuthentication,)

    @permit_if_role_in(['pravo-na-prosmotr-zadach'])
    def get(self, request):
        """Получаем задачи пользователя не зависимо от проекта"""
        try:
            tasks = get_task_user(request.user)
            serializer = self.serializer_class(tasks, many=True)
            return Response({'data': serializer.data,
                             'count': len(serializer.data)},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 400, 'message': e.__str__()},
                            status=status.HTTP_400_BAD_REQUEST)


class DetailUpdateTaskAPIView(APIView):
    """
    Получение одной задачи, обновление задачи,
    удаление задачи, списание часов в задачу
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = TaskSerializer
    authentication_classes = (JWTAuthentication,)

    @permit_if_role_in(['pravo-na-prosmotr-zadach'])
    def get(self, request, project_id, task_id):
        """Получение одной задачи"""
        try:
            task = get_one_task(project_id, task_id)
            serializer = self.serializer_class(task)
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        except Task.DoesNotExist as e:
            return Response({'status': 404, 'message': e.__str__()},
                            status=status.HTTP_404_NOT_FOUND)

    @permit_if_role_in(['pravo-na-spisanie-chasov-v-zadachu'])
    def post(self, request, project_id, task_id):
        """Списание часов в задачу"""
        try:
            task = track_task(project_id,
                              task_id,
                              request.user,
                              request.data.get('time_tracker'))
            serializer = self.serializer_class(task)
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        except Task.DoesNotExist as e:
            return Response({'status': 404, 'message': e.__str__()},
                            status=status.HTTP_404_NOT_FOUND)

    @permit_if_role_in(['pravo-na-redaktirovanie-zadach'])
    def patch(self, request, project_id, task_id):
        """Обновление одной задачи"""
        try:
            task = update_task(request.data,
                               project_id,
                               task_id,
                               request.user)
            serializer = self.serializer_class(task)
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        except User.DoesNotExist as e:
            return Response({'status': 404, 'message': e.__str__()},
                            status=status.HTTP_404_NOT_FOUND)
        except Task.DoesNotExist as e:
            return Response({'status': 404, 'message': e.__str__()},
                            status=status.HTTP_404_NOT_FOUND)

    @permit_if_role_in(['pravo-na-udalenie-zadach'])
    def delete(self, request, project_id, task_id):
        """Удаление задачи"""
        try:
            task = delete_task(project_id,
                               task_id,
                               request.user)
            serializer = self.serializer_class(task)
            return Response(serializer.data,
                            status=status.HTTP_204_NO_CONTENT)
        except Task.DoesNotExist as e:
            return Response({'status': 404, 'message': e.__str__()},
                            status=status.HTTP_404_NOT_FOUND)
