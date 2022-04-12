from django.urls import path

from fitness.terms.views import (
    CreateContactUsView,
    CreateFAQView,
    CreateGuidelinesView,
    CreatePrivacyPolicyView,
    CreateTermsView,
    GetContactUsView,
    GetFAQView,
    GetGuidelinesView,
    GetPrivacyPolicyView,
    GetTermsView,
)

urlpatterns = [
    path("add-terms/", CreateTermsView.as_view(), name="add-terms"),
    path("get-terms/", GetTermsView.as_view(), name="get-terms"),
    path(
        "add-guidelines/",
        CreateGuidelinesView.as_view(),
        name="add-guidelines",
    ),
    path(
        "get-guidelines/", GetGuidelinesView.as_view(), name="get-guidelines"
    ),
    path(
        "add-privacy-policy/",
        CreatePrivacyPolicyView.as_view(),
        name="add-privacy-policy",
    ),
    path(
        "get-privacy-policy/",
        GetPrivacyPolicyView.as_view(),
        name="get-privacy-policy",
    ),
    path("add-faq/", CreateFAQView.as_view(), name="add-faq"),
    path("get-faq/", GetFAQView.as_view(), name="get-faq"),
    path(
        "add-contact-us/", CreateContactUsView.as_view(), name="add-contact-us"
    ),
    path("get-contact-us/", GetContactUsView.as_view(), name="get-contact-us"),
]
