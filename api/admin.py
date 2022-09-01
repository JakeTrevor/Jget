# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Package


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'views', 'downloads', 'files')
    list_filter = ('creator',)
    raw_id_fields = ('authors', 'dependencies')
    search_fields = ('name',)
