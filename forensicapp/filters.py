import django_filters
from .models import *
class IncidentFilter(django_filters.FilterSet):
    #  filters 
    incident_location=django_filters.CharFilter(lookup_expr='icontains')
    incident_type=django_filters.CharFilter(lookup_expr='icontains')
    investigative_body=django_filters.CharFilter(lookup_expr='icontains')
    incident_date = django_filters.DateFilter()
    incident_date_range = django_filters.DateFromToRangeFilter(field_name="incident_date")

    class Meta:
        model = Incident
        fields = ['incident_location', 'incident_type', 'investigative_body' ,'incident_date' , 'incident_date_range']



class InspectionFilter(django_filters.FilterSet):
    #  filters 
    request_authority=django_filters.CharFilter(lookup_expr='icontains')
    incident =django_filters.CharFilter(lookup_expr='icontains')
    inspection_date = django_filters.DateFilter(field_name='inspection_date')
    inspection_date_range = django_filters.DateFromToRangeFilter(field_name="inspection_date")



    class Meta:
        model = InspectionForm
        fields = ['request_authority' , 'inspection_date' , 'incident' , 'inspection_date_range']

class FireFormFilter(django_filters.FilterSet):
    #  filters
    inspection_place=django_filters.CharFilter(lookup_expr='icontains')
    request_authority=django_filters.CharFilter(lookup_expr='icontains')
    incident_date = django_filters.DateFilter()
    inspection_date = django_filters.DateFilter()
    incident_date_range = django_filters.DateFromToRangeFilter(field_name="incident_date")
    inspection_date_range = django_filters.DateFromToRangeFilter(field_name="inspection_date")
    

    class Meta:
        model = FirePlaceDescribtion
        fields = ['inspection_place', 'request_authority', 'incident_date' , 'inspection_date' , 'incident_date_range' , 'inspection_date_range']
