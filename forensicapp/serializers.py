from rest_framework import serializers
from .models import *

class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = '__all__'



class IncidentStatisticsSerializer(serializers.Serializer):
    incident_type = serializers.CharField()
    count = serializers.IntegerField()



class EvidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evidence
        fields = '__all__'

class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = '__all__'

class InspectionFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = InspectionForm
        fields = '__all__'

