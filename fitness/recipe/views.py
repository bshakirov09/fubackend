import django_filters
from rest_framework import mixins, permissions
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from fitness.core.constants import PermissionTags
from fitness.core.permissions import UserStatusPermission
from fitness.recipe.filters import RecipeFilter
from fitness.recipe.models import Category, CategoryImage, Recipe
from fitness.recipe.serializers import (
    CategoryImageAdminSerializer,
    CategoryImageSerializer,
    CategoryListSerializer,
    CategorySerializer,
    RecipeAdminListSerializer,
    RecipeMiniSerializer,
    RecipeSerializer,
)


class CategoryViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    serializer_class = CategorySerializer
    image_serializer = CategoryImageSerializer
    queryset = Category.objects.all()
    view_tag = PermissionTags.RECIPE

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            self.permission_classes = (permissions.IsAdminUser,)
        else:
            self.permission_classes = (permissions.IsAuthenticated,)
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        queryset = Category.objects.all().order_by("order_number")
        image_queryset = CategoryImage.objects.all().order_by("order_number")
        serializer = CategoryListSerializer(queryset, many=True)
        image_serializer = self.image_serializer(
            image_queryset, many=True, context=self.get_serializer_context()
        )
        data = {"images": image_serializer.data, "categories": serializer.data}
        return Response(data)

    def perform_update(self, serializer):
        serializer.instance.update_by_order_number(serializer.validated_data)


class RecipeViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    filter_backends = (
        django_filters.rest_framework.DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
    )
    filter_class = RecipeFilter
    ordering_fields = ("id", "category")
    search_fields = ("id", "title")
    view_tag = PermissionTags.RECIPE

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            self.permission_classes = (permissions.IsAdminUser,)
        else:
            self.permission_classes = (UserStatusPermission,)
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "list":
            if self.request.user.is_staff:
                return RecipeAdminListSerializer
            return RecipeMiniSerializer
        return RecipeSerializer


class CategoryImageAdminViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    serializer_class = CategoryImageAdminSerializer
    queryset = CategoryImage.objects.all()
    permission_classes = (permissions.IsAdminUser,)

    def perform_create(self, serializer):
        serializer.instance = CategoryImage.objects.create_category_image(
            serializer.validated_data
        )
