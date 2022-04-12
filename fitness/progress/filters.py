import django_filters

from fitness.progress.models import Journal, Photo, Weight


class JournalFilter(django_filters.FilterSet):
    from_date = django_filters.DateFilter(
        field_name="created_dttm", lookup_expr="gte"
    )
    to_date = django_filters.DateFilter(
        field_name="created_dttm", lookup_expr="lte"
    )
    created_dttm = django_filters.DateFilter(
        field_name="created_dttm", lookup_expr="contains"
    )

    class Meta:
        model = Journal
        fields = ("created_dttm", "from_date", "to_date")


class WeightFilter(django_filters.FilterSet):
    from_date = django_filters.DateFilter(
        field_name="created_dttm", lookup_expr="gte"
    )
    to_date = django_filters.DateFilter(
        field_name="created_dttm", lookup_expr="lte"
    )
    created_dttm = django_filters.DateFilter(
        field_name="created_dttm", lookup_expr="contains"
    )

    class Meta:
        model = Weight
        fields = ("created_dttm", "from_date", "to_date")


class PhotoFilter(django_filters.FilterSet):
    from_date = django_filters.DateFilter(
        field_name="created_dttm", lookup_expr="gte"
    )
    to_date = django_filters.DateFilter(
        field_name="created_dttm", lookup_expr="lte"
    )
    created_dttm = django_filters.DateFilter(
        field_name="created_dttm", lookup_expr="contains"
    )

    class Meta:
        model = Photo
        fields = ("created_dttm", "from_date", "to_date")
