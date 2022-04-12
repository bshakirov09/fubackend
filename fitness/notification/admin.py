from django.contrib import admin

from .models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "recipient",
        "title",
        "message",
        "status",
        "notification_type",
    )
    list_filter = ("notification_type",)
    search_fields = ("id", "title", "message", "recipient")


admin.site.register(Notification, NotificationAdmin)
