from rest_framework import serializers

from fitness.terms.models import (
    FAQ,
    ContactUs,
    Guidelines,
    PrivacyPolicy,
    Terms,
)


class TermsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terms
        fields = ("description",)

    def create(self, validated_data):
        Terms.objects.update_or_create(
            pk=1, defaults=dict(description=validated_data["description"])
        )
        return validated_data


class GuidelinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guidelines
        fields = ("description",)

    def create(self, validated_data):
        Guidelines.objects.update_or_create(
            pk=1, defaults=dict(description=validated_data["description"])
        )
        return validated_data


class PrivacyPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivacyPolicy
        fields = ("description",)

    def create(self, validated_data):
        PrivacyPolicy.objects.update_or_create(
            pk=1, defaults=dict(description=validated_data["description"])
        )
        return validated_data


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ("description",)

    def create(self, validated_data):
        FAQ.objects.update_or_create(
            pk=1, defaults=dict(description=validated_data["description"])
        )
        return validated_data


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ("description",)

    def create(self, validated_data):
        ContactUs.objects.update_or_create(
            pk=1, defaults=dict(description=validated_data["description"])
        )
        return validated_data
