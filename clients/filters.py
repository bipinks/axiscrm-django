import django_filters
from django_filters.widgets import RangeWidget
from django_filters import FilterSet, DateFromToRangeFilter

from clients.models import ClientProject


class ClientProjectsFilter(FilterSet):
    # testt = django_filters.CharFilter(lookup_expr='iexact')

    # price = django_filters.NumberFilter()
    # client = django_filters.ChoiceFilter(field_name='client_id', label='CLLL')
    # price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')
    #
    # release_year = django_filters.NumberFilter(field_name='release_date', lookup_expr='year')
    next_amc_date = DateFromToRangeFilter(label='AMC Date Renewal Date Between',
                                          widget=RangeWidget(attrs=
                                                             {
                                                                 'display': 'inline',
                                                                 'class' : 'datepicker',
                                                                 'data-date-format':"yyyy-mm-dd",
                                                             }))
    # release_year__lt = django_filters.NumberFilter(field_name='release_date', lookup_expr='year__lt')

    # manufacturer__name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = ClientProject
        fields = ['client', 'project']
