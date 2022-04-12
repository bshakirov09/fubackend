from django.urls import path

from fitness.notification import views

urlpatterns = [
    path(
        "notification/",
        views.ListNotification.as_view(),
        name="notification-list",
    ),
    path(
        "notification/list-update/",
        views.NotificationListUpdateView.as_view(),
        name="update-notification-list",
    ),
    path(
        "status-update/",
        views.NotificationStatusUpdate.as_view(),
        name="status-update",
    ),
]
