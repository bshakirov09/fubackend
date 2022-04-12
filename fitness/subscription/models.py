from django.conf import settings
from django.db import models

from fitness.core.models import BaseModel
from fitness.subscription.constants import SubscriptionType
from fitness.subscription.managers import UserSubscriptionManager


class Subscription(models.Model):
    name = models.CharField(max_length=64, unique=True)
    type = models.CharField(
        max_length=64, choices=SubscriptionType.choices, unique=True
    )
    description = models.TextField()

    price_amount = models.DecimalField(
        max_digits=settings.MAX_DIGITS, decimal_places=settings.DECIMAL_PLACES
    )

    def __str__(self):
        return self.name


class UserSubscription(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_subscription",
    )
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE,
        related_name="user_subscriptions",
    )
    stripe_customer_id = models.CharField(max_length=255)
    stripe_subscription_id = models.CharField(max_length=255)
    is_trial = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = UserSubscriptionManager()

    class Meta:
        unique_together = ("user", "subscription")

    def __str__(self):
        return str(self.id)


class WebhookErrorLog(BaseModel):
    request_data = models.JSONField()
    event_type = models.CharField(max_length=255, blank=True, null=True)
    billing_reason = models.CharField(max_length=255, null=True, blank=True)
    error_message = models.TextField()
