from django.contrib import admin

from fitness.recipe.models import Category, CategoryImage, Recipe


class CategoryImageAdmin(admin.ModelAdmin):
    model = CategoryImage
    list_display = ("order_number",)


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = (
        "id",
        "title",
        "order_number",
    )
    search_fields = ("title",)


class RecipeAdmin(admin.ModelAdmin):
    model = Recipe
    list_display = (
        "title",
        "category",
    )
    search_fields = (
        "title",
        "category",
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(CategoryImage, CategoryImageAdmin)
