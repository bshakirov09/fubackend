import stripe
from django.conf import settings
from prompt_toolkit.validation import ValidationError
from stripe.error import InvalidRequestError


def create_customer_account(email):
    return stripe.Customer.create(
        api_key=settings.STRIPE_SECRET_KEY,
        email=email,
    )


def create_subscription(customer_id, price_id, trial_end):
    try:
        return stripe.Subscription.create(
            api_key=settings.STRIPE_SECRET_KEY,
            customer=customer_id,
            items=[
                {
                    "price": price_id,
                }
            ],
            payment_behavior="default_incomplete",
            expand=["latest_invoice.payment_intent"],
            trial_end=trial_end,
        )

    except InvalidRequestError as e:
        raise ValidationError(e.user_message)


def create_setup_intent(customer_id):
    try:
        return stripe.SetupIntent.create(
            api_key=settings.STRIPE_SECRET_KEY,
            customer=customer_id,
            payment_method_types=["card"],
        )
    except InvalidRequestError as e:
        raise ValidationError(e.user_message)
