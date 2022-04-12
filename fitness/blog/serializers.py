from rest_framework import serializers

from fitness.blog.models import Blog, BlogImages
from fitness.document.serializers import ImageModelSerializer


class BlogImagesMiniSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(source="image.file")

    class Meta:
        model = BlogImages
        fields = ("image",)


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = (
            "id",
            "title",
            "description",
            "podcast",
            "image",
            "blog_images",
            "created_dttm",
        )
        read_only_fields = ("blog_images",)

    def __init__(self, *args, **kwargs):
        super(BlogSerializer, self).__init__(*args, **kwargs)
        action = kwargs["context"]["view"].action
        if action == "retrieve":
            self.fields["image"] = serializers.SerializerMethodField()
            self.fields["blog_images"] = BlogImagesMiniSerializer(many=True)

    def get_image(self, obj):
        if obj.image:
            return obj.image.thumbnail_150.url
        return None


class BlogImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogImages
        fields = (
            "id",
            "blog",
            "image",
        )

    def __init__(self, *args, **kwargs):
        super(BlogImagesSerializer, self).__init__(*args, **kwargs)
        action = kwargs["context"]["view"].action
        if action in ["list", "retrieve"]:
            self.fields["image"] = ImageModelSerializer()


class BlogListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = (
            "id",
            "title",
            "image",
        )

    def get_image(self, obj):
        if obj.image:
            return obj.image.thumbnail_150.url
        return None
