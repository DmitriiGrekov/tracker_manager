from django.contrib import admin
from .models import Permission


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug',)
    list_display_links = ('name',)
    readonly_fields = ('slug',)
