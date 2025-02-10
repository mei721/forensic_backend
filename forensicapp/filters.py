import django_filters
from .models import Incident , InspectionForm 

class IncidentFilter(django_filters.FilterSet):
    #  filters for fields you want to filter on.
    incident_location=django_filters.CharFilter(lookup_expr='icontains')
    incident_type=django_filters.CharFilter(lookup_expr='icontains')
    investigative_body=django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Incident
        fields = ['incident_location', 'incident_type', 'investigative_body']

class InspectionFilter(django_filters.FilterSet):
    #  filters for fields you want to filter on.
    request_authority=django_filters.CharFilter(lookup_expr='icontains')
    incident =django_filters.CharFilter(lookup_expr='icontains')
    inspection_date = django_filters.DateFilter(field_name='inspection_date')


    class Meta:
        model = InspectionForm
        fields = ['request_authority' , 'inspection_date' , 'incident']
