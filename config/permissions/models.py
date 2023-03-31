from django.db import models
from django.utils.text import slugify


class Permission(models.Model):
    """Права доступа"""
    name = models.CharField('Название права',
                            max_length=300)
    slug = models.SlugField("Название на английском",
                            unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        return super(Permission, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Право'
        verbose_name_plural = 'Права'
