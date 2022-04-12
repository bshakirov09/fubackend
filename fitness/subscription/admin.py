from django.contrib import admin

from fitness.subscription.models import (
    Subscription,
    UserSubscription,
    WebhookErrorLog,
)

admin.site.register(Subscription)
admin.site.register(UserSubscription)
admin.site.register(WebhookErrorLog)
