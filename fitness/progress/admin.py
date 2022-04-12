from django.contrib import admin

from fitness.progress.models import Journal, Photo, Weight


@admin.register(Weight)
class WeightAdmin(admin.ModelAdmin):
    list_display = ["id", "weight", "created_dttm"]


admin.site.register(Journal)
admin.site.register(Photo)
