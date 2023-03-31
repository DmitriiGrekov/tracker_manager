from django.contrib import admin
from django.utils.html import mark_safe
from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'name',
                    'author',
                    'created_at',
                    'updated_at'
                    )
    list_display_links = ('name',)

    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="auto" height="200px" />')

    image_preview.short_description = 'Изображение компании'
