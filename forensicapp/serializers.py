from rest_framework import serializers
from .models import *

class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = '__all__'


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


class FirePlaceDescribtionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirePlaceDescribtion
        fields = '__all__'


class MapDescribtionSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = MapDescribtion
        fields = '__all__'