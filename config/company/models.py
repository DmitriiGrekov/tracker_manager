from django.db import models


class Company(models.Model):
    """Модель компании"""
    name = models.CharField(max_length=300,
                            verbose_name='Название компании',
                            unique=True)
    description = models.TextField(verbose_name='Описание компании',
                                   blank=True,
                                   null=True)
    image = models.ImageField(verbose_name='Изображение компании',
                              blank=True, null=True)
    author = models.ForeignKey('users.User', on_delete=models.SET_NULL,
                               verbose_name='Создатель компании',
                               null=True,
                               blank=True,
                               related_name='companies'
                               )
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Дата создания',
                                      )
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name='Дата обновления',
                                      )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'
        permissions = (
                ('can_update_company_permission', 'Право на обновление данных компании'),
                ('can_delete_company_permission', 'Право на удаление данных компании'),
                )
