from django.contrib import admin

from fitness.blog.models import Blog, BlogImages


class BlogAdmin(admin.ModelAdmin):
    model = Blog
    list_display = ("title",)
    search_fields = ("title",)


class BlogImagesAdmin(admin.ModelAdmin):
    model = BlogImages
    list_display = ("blog", "image")


admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogImages, BlogImagesAdmin)
