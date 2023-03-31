from django.contrib import admin
from django.utils.html import mark_safe
from .models import User


@admin.register(User)
class AdvUserAdmin(admin.ModelAdmin):
    """Пользователь"""
    list_display = ('id',
                    'email',
                    'username',
                    'first_name',
                    'last_name',
                    'last_login',
                    )
    list_display_links = ('email',
                          'username',)
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="auto" height="200px" />')

    image_preview.short_description = 'Изображение пользователя'


