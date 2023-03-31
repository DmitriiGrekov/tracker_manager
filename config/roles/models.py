from django.db import models
from django.utils.text import slugify
from permissions.models import Permission


class Role(models.Model):
    """Роли пользователя"""
    name = models.CharField(verbose_name='Название роли',
                            max_length=255)
    slug = models.SlugField(verbose_name='Slug',
                            unique=True)
    company = models.ForeignKey('company.Company',
                                on_delete=models.CASCADE,
                                verbose_name='Компания',
                                related_name='roles')
    permissions = models.ManyToManyField(Permission, verbose_name='Права')

    def save(self, *args, **kwargs):
        self.slug = slugify([self.name, self.company.name], allow_unicode=True)
        return super(Role, self).save(*args, **kwargs)

    def create_user_role_in_company(self):
        pass

    def __str__(self):
        return self.name

    @staticmethod
    def create_need_role(name: str, company, permissions):
        role = Role.objects.create(name=name, company=company)
        role.permissions.set(permissions)
        role.save()
        return role

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'
