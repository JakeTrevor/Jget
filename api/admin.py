# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import jgetUser, Package, File


@admin.register(jgetUser)
class jgetUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    list_filter = ('user',)


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    raw_id_fields = ('authors', 'dependencies')
    search_fields = ('name',)


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'fileName', 'content', 'package')
    list_filter = ('package',)
