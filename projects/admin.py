from django.contrib import admin

from .models import Projects
from django import forms

# Register your models here.


@admin.register(Projects)
class ProjectAdmin(admin.ModelAdmin):
    readonly_fields = ['creation_date']
    list_display = ['name', ]
