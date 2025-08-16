from django.contrib import admin
from .models import DownloadLog

@admin.register(DownloadLog)
class DownloadLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'filename', 'downloaded_at')
    list_filter = ('downloaded_at',)
    search_fields = ('user__username', 'filename')
