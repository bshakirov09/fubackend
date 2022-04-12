from django.contrib import admin
from django.urls import include, path

from fitness.core.swagger import urlpatterns as doc_urls

urlpatterns = doc_urls

urlpatterns += [
    path("admin/", admin.site.urls),
    path("v1/account/", include("fitness.account.urls")),
    path("v1/", include("fitness.document.urls")),
    path("v1/", include("fitness.recipe.urls")),
    path("v1/", include("fitness.core.urls")),
    path("v1/", include("fitness.blog.urls")),
    path("v1/", include("fitness.workout.urls")),
    path("v1/", include("fitness.progress.urls")),
    path("v1/", include("fitness.terms.urls")),
    path("v1/", include("fitness.subscription.urls")),
    path("v1/", include("fitness.notification.urls")),
]
