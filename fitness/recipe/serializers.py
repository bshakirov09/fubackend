from rest_framework import serializers

from fitness.document.serializers import ImageModelSerializer
from fitness.recipe.models import Category, CategoryImage, Recipe


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "title", "order_number")


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "title")


class CategoryImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(source="image.file")

    class Meta:
        model = CategoryImage
        fields = (
            "id",
            "image",
        )


class CategoryImageAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryImage
        fields = ("id", "image", "order_number")

        extra_kwargs = {"order_number": {"read_only": True}}

    def __init__(self, *args, **kwargs):
        super(CategoryImageAdminSerializer, self).__init__(*args, **kwargs)
        action = kwargs["context"]["view"].action
        if action in ["list", "retrieve"]:
            self.fields["image"] = ImageModelSerializer()


class RecipeMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            "id",
            "title",
        )


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            "id",
            "title",
            "category",
            "vegetarian_ingredients",
            "ingredients",
        )

    def __init__(self, *args, **kwargs):
        super(RecipeSerializer, self).__init__(*args, **kwargs)
        action = kwargs["context"]["view"].action
        if action == "retrieve":
            self.fields["category"] = CategoryListSerializer()


class RecipeAdminListSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "title",
            "category",
        )
