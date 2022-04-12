import random

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.postgres.fields import ArrayField
from django.core.cache import cache
from django.db import models
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

from fitness.account.constants import GENDER, AuthType
from fitness.account.managers import UserManager
from fitness.document.models import ImageModel
from fitness.notification.constants import NotificationType


class User(AbstractBaseUser, PermissionsMixin):
    class UserStatus(models.TextChoices):
        ACTIVE = "active"
        BLOCKED = "blocked"
        RESTRICTED = "restricted"

    email = models.EmailField("email", unique=True)
    first_name = models.CharField("first name", max_length=150)
    last_name = models.CharField("last name", max_length=150, blank=True)
    full_name = models.CharField("full name", max_length=150, blank=True)
    profile_image = models.ForeignKey(
        ImageModel, on_delete=models.SET_NULL, null=True, blank=True
    )
    gender = models.CharField(
        choices=GENDER.choices, max_length=15, null=True, blank=True
    )
    height = models.DecimalField(
        max_digits=settings.MAX_DIGITS,
        decimal_places=settings.DECIMAL_PLACES,
        null=True,
        blank=True,
    )
    weight = models.DecimalField(
        max_digits=settings.MAX_DIGITS,
        decimal_places=settings.DECIMAL_PLACES,
        null=True,
        blank=True,
    )
    devices = ArrayField(
        models.CharField(max_length=255), blank=True, default=list
    )
    auth_type = models.CharField(
        max_length=50, choices=AuthType.choices, null=True, blank=True
    )
    is_staff = models.BooleanField(
        "staff status",
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    is_active = models.BooleanField(
        "active",
        default=True,
        help_text=(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField("date joined", default=timezone.now)
    date_of_birth = models.DateField(blank=True, null=True)
    status = models.CharField(
        max_length=50,
        choices=UserStatus.choices,
        default=UserStatus.RESTRICTED,
    )
    notification_settings = ArrayField(
        models.CharField(
            max_length=50,
            choices=NotificationType.choices,
        ),
        default=NotificationType.get_default_types,
    )
    objects = UserManager()

    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return f"{self.email}"

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def save(self, *args, **kwargs):
        self.full_name = f"{self.first_name} {self.last_name}"
        super(User, self).save(*args, **kwargs)

    @classmethod
    def generate_code(cls):
        return random.randint(1000, 9999)

    @classmethod
    def set_cache(cls, key, val, ttl=300):
        cache.set(f"{key}", val, timeout=ttl)

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}

    def get_notification_settings(self):
        result = {}
        for key in NotificationType.get_default_types():
            result[key] = True if key in self.notification_settings else False
        return result

    def update_notification_settings(self, data):
        notification_list = [
            key
            for key, val in data.items()
            if val and key in NotificationType.get_changeable_types()
        ]
        self.notification_settings = (
            notification_list + NotificationType.get_constant_types()
        )
        self.save()
