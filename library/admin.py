from django.contrib import admin
from .models import DownloadLog, FilePermission

@admin.register(DownloadLog)
class DownloadLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'filename', 'downloaded_at')
    list_filter = ('downloaded_at',)
    search_fields = ('user__username', 'filename')

@admin.register(FilePermission)
class FilePermissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'filename', 'granted_at')
    list_filter = ('granted_at',)
    search_fields = ('user__username', 'filename')
