import django_filters
from .models import *
class IncidentFilter(django_filters.FilterSet):
    # Filters based on text content
    date_discovery = django_filters.CharFilter(lookup_expr='icontains')
    action_taken = django_filters.CharFilter(lookup_expr='icontains')
    
    # Filters based on specific date fields
    incident_date = django_filters.DateFilter()
    incident_date_range = django_filters.DateFromToRangeFilter(field_name="accident_date")
    
    # Filters based on category choices
    category_accident = django_filters.ChoiceFilter(choices=[('fireAccident', 'Fire Accident'), ('accident', 'Accident')])
    
    # Filters based on status and location
   
    accident_location = django_filters.CharFilter(lookup_expr='icontains')
    
    # Filters based on geographical coordinates
    latitude = django_filters.CharFilter(lookup_expr='icontains')
    longitude = django_filters.CharFilter(lookup_expr='icontains')
    
    # Filters for the user  (assuming you have a 'CustomUser' model)
    user = django_filters.ModelChoiceFilter(queryset=CustomUser.objects.all(), null_label="Any User")
    
    # Additional filters for specific fields
    inspecting_body = django_filters.CharFilter(lookup_expr='icontains')
    investigating_body = django_filters.CharFilter(lookup_expr='icontains')
    typeAccident = django_filters.CharFilter(lookup_expr='icontains')
    color = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Incident
        fields = [
            'date_discovery', 'action_taken',  
             'incident_date', 'incident_date_range', 
            'category_accident','latitude', 'longitude', 
            'user', 'typeAccident', 'color', 'investigating_body'
        ]


class InspectionFilter(django_filters.FilterSet):
    #  filters 
    request_authority=django_filters.CharFilter(lookup_expr='icontains')
    incident =django_filters.CharFilter(lookup_expr='icontains')
    inspection_date = django_filters.DateFilter(field_name='inspection_date')
    inspection_date_range = django_filters.DateFromToRangeFilter(field_name="inspection_date")



    class Meta:
        model = InspectionForm
        fields = ['request_authority' , 'inspection_date' , 'incident' , 'inspection_date_range']

