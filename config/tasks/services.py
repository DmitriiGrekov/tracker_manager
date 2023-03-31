from .serializers import TaskFileSerializer, TaskSerializer
from .models import Task, TaskFiles

from users.models import User
from projects.services import get_one_project


def get_all_task_project(project_id: int, user: User) -> list[Task]:
    """Получение задач проекта"""
    project = get_one_project(project_id,
                              user.id)
    return project.tasks.all()


def get_task_user(user: User) -> list[Task]:
    """Получение задач пользователя"""
    tasks = Task.objects.filter(executor=user)
    return tasks


def get_one_task(project_id: int, task_id: int) -> Task:
    """Получение одной задачи"""
    task = Task.objects.get(project__id=project_id,
                            pk=task_id)
    return task


def create_task(validated_data, project_id: int, user: User) -> Task:
    """Создание задачи"""
    project = get_one_project(project_id,
                              user.id)
    serializer = TaskSerializer(data=validated_data)
    serializer.is_valid(raise_exception=True)
    task = serializer.save(author=user,
                           project=project,
                           company=user.company)
    executor = _get_executor_from_data(validated_data, task)
    task.executor = executor
    task.save()
    return task


def update_task(validated_data, project_id: int, task_id: int,
                user: User) -> Task:
    """Обновление задачи"""
    task = Task.objects.get(project__id=project_id,
                            pk=task_id,
                            author=user)
    executor = _get_executor_from_data(validated_data, task)
    serializer = TaskSerializer(task,
                                data=validated_data,
                                partial=True)
    serializer.is_valid(raise_exception=True)
    task = serializer.save(executor=executor)
    return task


def delete_task(project_id: int, task_id: int, user: User) -> Task:
    """Удаление задачи"""
    task = Task.objects.get(pk=task_id,
                            project__id=project_id,
                            author=user)
    task.delete()
    return task


def track_task(project_id: int, task_id: int, user: User,
               time_tracker: int) -> Task:
    """Списание часов в задачу исполнителем"""
    task = Task.objects.get(pk=task_id,
                            project__id=project_id,
                            executor=user)
    serializer = TaskSerializer(task,
                                data={'time_tracker': time_tracker},
                                partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return task


def _get_executor_from_data(validated_data, task: Task) -> User:
    """Получаем пользователя из BODY данных"""
    executor_id = validated_data.get('executor')
    if not executor_id:
        return task.executor
    executor = User.objects.get(pk=executor_id,
                                company=task.company)
    return executor
