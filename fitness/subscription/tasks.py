import json

import stripe
from django.conf import settings
from django.contrib.auth import get_user_model

from fitness.celery import app
from fitness.notification.constants import NotificationType
from fitness.notification.models import Notification
from fitness.subscription.models import UserSubscription, WebhookErrorLog
from fitness.websocket.utils import send_data_to_channel


@app.task
def webhook(request_data, signature):
    user = None
    message = str()
    message_type = None
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET
    json_data = json.loads(request_data)
    if webhook_secret:
        try:
            event = stripe.Webhook.construct_event(
                api_key=settings.STRIPE_SECRET_KEY,
                payload=request_data,
                sig_header=signature,
                secret=webhook_secret,
            )
            data = event["data"]
        except Exception as e:
            WebhookErrorLog.objects.create(
                request_data=json_data,
                event_type=json_data["type"],
                billing_reason=json_data["data"]["object"].get(
                    "billing_reason"
                ),
                error_message=e,
            )
            return
        event_type = event["type"]
    else:
        data = request_data["data"]
        event_type = request_data["type"]

    data_object = data["object"]
    billing_reason = data_object.get("billing_reason")
    if event_type == "invoice.payment_succeeded":
        if billing_reason == "subscription_create":
            subscription_id = data_object["subscription"]
            payment_intent_id = data_object["payment_intent"]

            payment_intent = stripe.PaymentIntent.retrieve(
                payment_intent_id, api_key=settings.STRIPE_SECRET_KEY
            )

            stripe.Subscription.modify(
                subscription_id,
                api_key=settings.STRIPE_SECRET_KEY,
                default_payment_method=payment_intent.payment_method,
            )
            user_subscription = UserSubscription.objects.filter(
                stripe_subscription_id=subscription_id
            ).first()
            if user_subscription:
                if not user_subscription.is_active:
                    message = "subscription_activated"
                    message_type = "subscription"
                user_subscription.is_active = True
                user_subscription.save()
                user = user_subscription.user
                user.status = get_user_model().UserStatus.ACTIVE
                user.save()
                additional_data = {
                    "subscription_name": user_subscription.subscription.name,
                    "description": user_subscription.subscription.description,
                    "subscription_price": str(
                        user_subscription.subscription.price_amount
                    ),
                }
                Notification.objects.create(
                    recipient=user,
                    title="New notification",
                    message="Your subscription payment has been succeeded",
                    notification_type=NotificationType.SUBSCRIPTION,
                    additional_data=additional_data,
                )

    elif event_type == "invoice.payment_failed":
        if billing_reason == "subscription_create":
            subscription_id = data_object["subscription"]
            user_subscription = UserSubscription.objects.filter(
                stripe_subscription_id=subscription_id
            ).first()
            if user_subscription:
                user_subscription.is_active = False
                user_subscription.save()
                user = user_subscription.user
                user.status = get_user_model().UserStatus.RESTRICTED
                user.save()
                message = "payment_failed"
                message_type = "subscription"
    elif event_type == "invoice.finalized":
        pass
    elif event_type == "invoice.upcoming":
        pass

    elif event_type == "customer.subscription.deleted":
        if billing_reason == "subscription_create":
            subscription_id = data_object["subscription"]
            user_subscription = UserSubscription.objects.filter(
                stripe_subscription_id=subscription_id
            ).first()
            if user_subscription:
                user = user_subscription.user
                user.status = get_user_model().UserStatus.RESTRICTED
                user.save()
                user_subscription.delete()
                message = "subscription_deleted"
                message_type = "subscription"
    if user and message_type:
        send_data_to_channel(
            user.id,
            message_type,
            {"type": message_type, "message": message},
        )
