from django.db import models
from users.models import User
from projects.models import Project
from company.models import Company


class Task(models.Model):
    """Модель задач"""
    TASK_STATUS = (
            ('new', 'Новая'),
            ('on_hold', 'OnHold'),
            ('back_log', 'BackLog'),
            ('to_estimate', 'ToEstimate'),
            ('to_do', 'ToDo'),
            ('in_progress', 'InProgress'),
            ('dev', 'Dev'),
            ('test', 'Test'),
            ('pause', 'Пауза'),
            ('solved', 'Решена')
            )
    name = models.CharField(verbose_name='Название задачи',
                            max_length=300)
    description = models.TextField(verbose_name='Описание задачи',
                                   blank=True,
                                   null=True)
    author = models.ForeignKey(User,
                               on_delete=models.SET_NULL,
                               verbose_name='Автор задачи',
                               related_name='task_author',
                               null=True,
                               blank=True
                               )
    executor = models.ForeignKey(User,
                                 on_delete=models.SET_NULL,
                                 verbose_name='Исполнитель',
                                 blank=True,
                                 null=True,
                                 related_name='task_executor'
                                 )
    project = models.ForeignKey(Project,
                                on_delete=models.CASCADE,
                                verbose_name='Проект',
                                related_name='tasks')
    company = models.ForeignKey(Company,
                                on_delete=models.CASCADE,
                                verbose_name='Компания',
                                related_name='tasks')
    date_sprint = models.DateTimeField(verbose_name='Дата окончания работы над задачей',
                                       blank=True,
                                       null=True)
    status = models.CharField(verbose_name='Статус задачи',
                              choices=TASK_STATUS,
                              default='new',
                              max_length=300)
    time_tracker = models.IntegerField(verbose_name='Число затреканных часов',
                                       default=0)
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name='Дата обновления')

    def __str__(self):
        return f'{self.company.name} -> {self.project.name} -> {self.name}'

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


class TaskFiles(models.Model):
    """Модель файлов к задачам"""
    file = models.FileField(upload_to="tasks/%Y/%m/%d",
                            verbose_name='Файл')
    task = models.ForeignKey(Task,
                             on_delete=models.CASCADE,
                             related_name='files',
                             verbose_name='Задача'
                             )

    def __str__(self):
        return f'{self.task.name}-file'

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
