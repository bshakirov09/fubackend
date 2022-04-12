from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from fitness.terms.models import (
    FAQ,
    ContactUs,
    Guidelines,
    PrivacyPolicy,
    Terms,
)
from fitness.terms.serializers import (
    ContactUsSerializer,
    FAQSerializer,
    GuidelinesSerializer,
    PrivacyPolicySerializer,
    TermsSerializer,
)


class CreateTermsView(CreateAPIView):
    serializer_class = TermsSerializer
    permission_classes = (permissions.IsAdminUser,)


class GetTermsView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = TermsSerializer

    def get(self, *args, **kwargs):
        queryset = Terms.objects.all().first()
        serializer = self.serializer_class(instance=queryset)
        return Response(serializer.data)


class CreateGuidelinesView(CreateAPIView):
    serializer_class = GuidelinesSerializer
    permission_classes = (permissions.IsAdminUser,)


class GetGuidelinesView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = GuidelinesSerializer

    def get(self, *args, **kwargs):
        queryset = Guidelines.objects.all().first()
        serializer = self.serializer_class(instance=queryset)
        return Response(serializer.data)


class CreatePrivacyPolicyView(CreateAPIView):
    serializer_class = PrivacyPolicySerializer
    permission_classes = (permissions.IsAdminUser,)


class GetPrivacyPolicyView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = PrivacyPolicySerializer

    def get(self, *args, **kwargs):
        queryset = PrivacyPolicy.objects.all().first()
        serializer = self.serializer_class(instance=queryset)
        return Response(serializer.data)


class CreateFAQView(CreateAPIView):
    serializer_class = FAQSerializer
    permission_classes = (permissions.IsAdminUser,)


class GetFAQView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = FAQSerializer

    def get(self, *args, **kwargs):
        queryset = FAQ.objects.all().first()
        serializer = self.serializer_class(instance=queryset)
        return Response(serializer.data)


class CreateContactUsView(CreateAPIView):
    serializer_class = ContactUsSerializer
    permission_classes = (permissions.IsAdminUser,)


class GetContactUsView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ContactUsSerializer

    def get(self, *args, **kwargs):
        queryset = ContactUs.objects.all().first()
        serializer = self.serializer_class(instance=queryset)
        return Response(serializer.data)
