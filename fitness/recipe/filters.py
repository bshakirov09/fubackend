import django_filters

from fitness.recipe.models import Recipe


class RecipeFilter(django_filters.FilterSet):
    class Meta:
        model = Recipe
        fields = ("category",)
