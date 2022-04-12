from django.contrib.auth import get_user_model
from rest_framework import permissions

from fitness.core.constants import PermissionTags


class UserStatusPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            self.message = "You are not authorized"
            return False
        view_tag = getattr(view, "view_tag", None)
        if view_tag is None:
            return True
        if user.status == get_user_model().UserStatus.ACTIVE:
            return True
        elif user.status == get_user_model().UserStatus.RESTRICTED:
            if view_tag in PermissionTags.get_unrestricted_tags():
                return True
            else:
                self.message = (
                    "Your profile is restricted for this "
                    "content! Because your subscription "
                    "payment has not been succeeded yet"
                )
                return False
        else:
            self.message = "You have been blocked!"
            return False
