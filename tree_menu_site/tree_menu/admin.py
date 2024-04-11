from django.contrib import admin

from .forms import MenuForm
from .models import Menu


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'parent']
    prepopulated_fields = {'slug': ('name', )}
    form = MenuForm
