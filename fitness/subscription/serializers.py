from rest_framework import serializers

from fitness.subscription.models import Subscription, UserSubscription


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = (
            "id",
            "name",
            "description",
            "price_amount",
        )


class SubscriptionMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = (
            "id",
            "name",
            "price_amount",
        )


class UserSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubscription
        fields = (
            "id",
            "subscription",
            "is_trial",
        )

    def __init__(self, *args, **kwargs):
        super(UserSubscriptionSerializer, self).__init__(*args, **kwargs)
        action = kwargs["context"]["view"].action
        if action == "my_subscription":
            self.fields["subscription"] = serializers.CharField(
                source="subscription.name"
            )
