# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Package, File


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator')
    list_filter = ('creator',)
    raw_id_fields = ('authors', 'dependencies')
    search_fields = ('name',)


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('fileName', 'content', 'package')
    list_filter = ('package',)
