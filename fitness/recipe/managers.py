from django.db import models


class CategoryManager(models.Manager):
    pass


class RecipeManager(models.Manager):
    pass


class CategoryImageManager(models.Manager):
    def create_category_image(self, data):
        numbers = self.all().values_list("order_number", flat=True)
        order_number = max(numbers) + 1 if numbers else 1
        data["order_number"] = order_number
        self.create(**data)
