from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify
from datetime import datetime, timedelta
from django.conf import settings
import jwt

from roles.models import Role
from company.models import Company


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users must have a username.')
        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError('Superusers must have a password')
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractUser, PermissionsMixin):
    """Модель кастомного пользователя"""
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    about = models.TextField(null=True, blank=True, verbose_name='О себе')
    is_active = models.BooleanField(default=True,
                                    verbose_name='Пользователь активен')
    is_staff = models.BooleanField(default=False,
                                   verbose_name='Доступ к админ панели')
    company = models.ForeignKey(Company,
                                on_delete=models.SET_NULL,
                                verbose_name='Компания',
                                blank=True,
                                null=True,
                                related_name='users'
                                )
    roles = models.ManyToManyField(Role, verbose_name='Роли')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    image = models.ImageField(verbose_name='Изображение пользователя',
                              blank=True,
                              null=True
                              )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]
    objects = UserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name} -> {self.email}'

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=365)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
            }, settings.SECRET_KEY, algorithm='HS256')
        return token.decode('utf-8')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
