from django.db import models
from users.models import User
from company.models import Company


class Project(models.Model):
    name = models.CharField(max_length=300,
                            verbose_name='Название проекта')
    description = models.TextField(verbose_name='Описание проекта',
                                   blank=True,
                                   null=True)
    users = models.ManyToManyField(User,
                                   verbose_name='Пользователи',
                                   related_name='projects')
    company = models.ForeignKey(Company,
                                on_delete=models.CASCADE,
                                verbose_name='Компания',
                                related_name='projects')
    is_active = models.BooleanField(verbose_name='Активность проекта',
                                    default=True)
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name='Дата обновления проекта')

    def __str__(self):
        return f'{self.company.name} -> {self.name}'

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
