import calendar
from datetime import datetime, timedelta

import django_filters
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from fitness.core.pagination import ProgressPagination
from fitness.progress.constants import Direction
from fitness.progress.filters import JournalFilter, PhotoFilter, WeightFilter
from fitness.progress.models import Journal, Photo, Weight
from fitness.progress.serializers import (
    CalculateMacrosIntakeSerializer,
    CalculatorRMRSerializer,
    JournalListSerializer,
    JournalSerializer,
    PhotoDetailNextSerializer,
    PhotoSerializer,
    WeightSerializer,
)
from fitness.progress.utils import (
    calculate_macronutrient_intake,
    calculate_macronutrients,
    calculate_rmr,
)


class WeightViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = Weight.objects.all()
    serializer_class = WeightSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = WeightFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance)
        result = serializer.data
        photo = Photo.objects.filter(
            created_dttm__date=instance.created_dttm.date()
        ).last()
        journal = Journal.objects.filter(
            created_dttm__date=instance.created_dttm.date()
        ).last()
        result["photo"] = (
            PhotoSerializer(photo, context=self.get_serializer_context()).data
            if photo
            else {}
        )
        result["journal"] = (
            JournalSerializer(
                journal, context=self.get_serializer_context()
            ).data
            if journal
            else {}
        )
        return Response(result)

    @action(methods=["GET"], detail=False, url_path="add-weight-check")
    def add_weight_check(self, request):
        qs = self.queryset.filter(created_dttm__date=datetime.now().date())
        if qs.exists():
            serializer = self.serializer_class(
                qs.first(), many=False, context=self.get_serializer_context()
            )
            return Response(serializer.data)
        return Response({})

    @action(methods=["GET"], detail=False, url_path="weekly")
    def weekly(self, request):
        now = datetime.now()
        today = now.date()
        week = list(calendar.day_abbr)
        start_week = today - timedelta(today.weekday())
        end_week = start_week + timedelta(len(week))
        qs = self.queryset.filter(
            created_dttm__date__range=[start_week, end_week]
        ).order_by("created_dttm")
        exist_data = dict()
        for obj in qs:
            exist_data[obj.created_dttm.strftime("%a")] = {
                "id": obj.id,
                "weight": obj.weight,
            }
        result = dict()
        for i, day in enumerate(week):
            result[day] = exist_data.get(day)
        return Response(result)

    @action(methods=["GET"], detail=False, url_path="monthly")
    def monthly(self, request):
        now = datetime.now()
        date_range = [
            day
            for day in calendar.Calendar().itermonthdates(now.year, now.month)
            if day.month == now.month
        ]
        qs = self.queryset.filter(created_dttm__date__in=date_range)
        exist_data = dict()
        for weight in qs:
            exist_data[int(weight.created_dttm.strftime("%d"))] = {
                "id": weight.id,
                "weight": weight.weight,
            }
        result = dict()
        for i in range(1, len(date_range)):
            result[i] = exist_data.get(i)
        return Response(result)

    @action(methods=["GET"], detail=False, url_path="yearly")
    def yearly(self, request):
        result = dict()
        year = datetime.now().year
        for month in range(1, 13):
            weight = self.queryset.filter(
                created_dttm__month=month, created_dttm__year=year
            ).last()
            result[calendar.month_abbr[month]] = (
                {"id": weight.id, "weight": weight.weight} if weight else None
            )
        return Response(result)


class PhotoViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = PhotoFilter
    pagination_class = ProgressPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=["GET"], detail=False, url_path="add-photo-check")
    def add_photo_check(self, request):
        qs = self.queryset.filter(created_dttm__date=datetime.now().date())
        if qs.exists():
            serializer = self.serializer_class(
                qs.first(), many=False, context=self.get_serializer_context()
            )
            return Response(serializer.data)
        return Response({})

    @action(
        methods=["POST"],
        detail=False,
        url_path="detail-view",
        serializer_class=PhotoDetailNextSerializer,
    )
    def detail_view(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        current_date = data.get("current_date")
        if data.get("direction") == Direction.NEXT:
            qs = self.queryset.filter(
                created_dttm__date__gt=current_date
            ).order_by("created_dttm")
        else:
            qs = self.queryset.filter(
                created_dttm__date__lt=current_date
            ).order_by("-created_dttm")
        if qs.exists():
            serializer = PhotoSerializer(
                qs.first(), many=False, context=self.get_serializer_context()
            )
            return Response(serializer.data)
        return Response({})


class JournalViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    queryset = Journal.objects.all()
    serializer_class = JournalSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = JournalFilter
    pagination_class = ProgressPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return JournalListSerializer
        return self.serializer_class

    @action(methods=["GET"], detail=False, url_path="add-journal-check")
    def add_journal_check(self, request):
        photos = self.queryset.filter(created_dttm__date=datetime.now().date())
        if photos.exists():
            serializer = self.serializer_class(
                photos.first(),
                many=False,
                context=self.get_serializer_context(),
            )
            return Response(serializer.data)
        return Response({})


class CalculatorRMRView(APIView):
    serializer_class = CalculatorRMRSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        rmr = calculate_rmr(validated_data)
        return Response(
            calculate_macronutrients(rmr, validated_data.get("weight"))
        )


class CalculateMacronutrientIntakeView(APIView):
    serializer_class = CalculateMacrosIntakeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            calculate_macronutrient_intake(serializer.validated_data)
        )
