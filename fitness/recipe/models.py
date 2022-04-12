from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from fitness.core.constants import PageChoices
from fitness.core.models import BaseModel, VersionControl
from fitness.document.models import ImageModel
from fitness.recipe.managers import (
    CategoryImageManager,
    CategoryManager,
    RecipeManager,
)


class CategoryImage(BaseModel):
    image = models.ForeignKey(ImageModel, on_delete=models.SET_NULL, null=True)
    order_number = models.PositiveIntegerField()

    objects = CategoryImageManager()


class Category(BaseModel):
    title = models.CharField(max_length=255)
    order_number = models.PositiveIntegerField(null=True)

    objects = CategoryManager()

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def update_by_order_number(self, data):
        order_number = data.get("order_number")
        old_category = Category.objects.filter(
            order_number=order_number
        ).first()
        if old_category:
            old_category.order_number = self.order_number
            old_category.save()
        self.order_number = order_number
        self.save()
        return self


class Recipe(BaseModel):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="recipes",
        related_query_name="recipe",
    )
    vegetarian_ingredients = ArrayField(
        models.CharField(max_length=500), blank=True, default=list
    )
    ingredients = ArrayField(
        models.CharField(max_length=500), blank=True, default=list
    )

    objects = RecipeManager()

    class Meta:
        verbose_name = _("recipe")
        verbose_name_plural = _("recipes")


@receiver([post_save], sender=Category)
def change_category_version(instance, **kwargs):
    version, created = VersionControl.objects.get_or_create(
        page=PageChoices.RECIPE_CATEGORY, detail_id=None
    )
    if not created:
        version.version += 1
        version.save()


@receiver([post_save], sender=Recipe)
def change_recipe_version(instance, **kwargs):
    version, created = VersionControl.objects.get_or_create(
        page=PageChoices.RECIPE, detail_id=instance.category.id
    )
    if not created:
        version.version += 1
        version.save()


@receiver([post_save], sender=Recipe)
def change_recipe_detail_version(instance, **kwargs):
    version, created = VersionControl.objects.get_or_create(
        page=PageChoices.RECIPE_DETAIL, detail_id=instance.id
    )
    if not created:
        version.version += 1
        version.save()
