from datetime import datetime, timedelta

from django.conf import settings
from django.db import models

from fitness.subscription.constants import SubscriptionType
from fitness.subscription.utils import (
    create_customer_account,
    create_subscription,
)


class UserSubscriptionManager(models.Manager):
    def create_user_subscription(self, data, user):
        customer = create_customer_account(user.email)
        if data["subscription"].type == SubscriptionType.YEARLY:
            price_id = settings.STRIPE_PRICE_ID_YEARLY
        else:
            price_id = settings.STRIPE_PRICE_ID_MONTHLY
        if data["is_trial"]:
            trial_end = datetime.utcnow() + timedelta(
                days=int(settings.SUBSCRIPTION_TRIAL_DAYS)
            )
        else:
            trial_end = None
        stripe_subscription = create_subscription(
            customer.id, price_id, trial_end
        )
        result = {
            "invoice_url": stripe_subscription["latest_invoice"][
                "hosted_invoice_url"
            ],
            "invoice_pdf": stripe_subscription["latest_invoice"][
                "invoice_pdf"
            ],
        }
        if data["is_trial"]:
            data["is_active"] = True
            result["client_secret"] = None
        else:
            data["is_active"] = False
            result["client_secret"] = stripe_subscription["latest_invoice"][
                "payment_intent"
            ]["client_secret"]
        data["stripe_customer_id"] = customer.id
        data["stripe_subscription_id"] = stripe_subscription.id
        data["user"] = user
        self.create(**data)
        return result
