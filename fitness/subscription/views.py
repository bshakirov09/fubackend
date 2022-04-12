from rest_framework import mixins, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from fitness.subscription.models import Subscription, UserSubscription
from fitness.subscription.serializers import (
    SubscriptionSerializer,
    UserSubscriptionSerializer,
)
from fitness.subscription.tasks import webhook


class SubscriptionViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            self.permission_classes = (permissions.IsAdminUser,)
        else:
            self.permission_classes = (permissions.IsAuthenticated,)
        return super().get_permissions()


class UserSubscriptionViewSet(
    mixins.CreateModelMixin, mixins.UpdateModelMixin, GenericViewSet
):
    queryset = UserSubscription.objects.all()
    serializer_class = UserSubscriptionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        client_secret = UserSubscription.objects.create_user_subscription(
            serializer.validated_data, self.request.user
        )
        return Response(client_secret, status=status.HTTP_201_CREATED)

    @action(methods=["GET"], detail=False, url_path="my")
    def my_subscription(self, request):
        user = request.user
        subscription = self.queryset.filter(user=user).first()
        if subscription:
            serializer = self.serializer_class(
                subscription, context=self.get_serializer_context()
            )
            return Response(serializer.data)
        else:
            return Response({})


class SubscriptionWebhook(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        request_data = request.body
        signature = request.headers.get("stripe-signature")
        webhook(request_data, signature)
        return Response({"status": "success"})
