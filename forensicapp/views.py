from django.shortcuts import render
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from .pagination import CustomPaginationWithResult
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import filters
from .filters import IncidentFilter,InspectionFilter
from django_filters.rest_framework import DjangoFilterBackend



class BaseAPIView(APIView):
    model = None
    serializer_class = None

    def get(self, request, pk=None):
        if pk:
            try:
                instance = self.model.objects.get(pk=pk)
                serializer = self.serializer_class(instance)
                return Response({"data": serializer.data})
            except self.model.DoesNotExist:
                return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            paginator = CustomPaginationWithResult()
            instances = self.model.objects.all().order_by('-id')
            result_page = paginator.paginate_queryset(instances, request)
            serializer = self.serializer_class(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            instance = self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            instance = self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        instance.delete()
        return Response({'message': 'Deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
class IncindentView(BaseAPIView):
    model = Incident
    serializer_class = IncidentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = IncidentFilter
    def get(self, request):
        # Get the filtered queryset
        queryset = self.model.objects.all().order_by('-id')
        filtered_queryset = IncidentFilter(request.GET, queryset=queryset).qs
        serializer = self.serializer_class(filtered_queryset, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)




class EvidenceView(BaseAPIView):
    model = Evidence
    serializer_class = EvidenceSerializer


class ComplaintView(BaseAPIView):
    model = Complaint
    serializer_class = ComplaintSerializer

class InspectionFormView(BaseAPIView):
    model  = InspectionForm
    serializer_class = InspectionFormSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = InspectionFilter
    def get(self, request):
        # Get the filtered queryset
        queryset = self.model.objects.all().order_by('-id')
        filtered_queryset = InspectionFilter(request.GET, queryset=queryset).qs
        serializer = self.serializer_class(filtered_queryset, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)



class FirePlaceDescribtionView(BaseAPIView):
    model = FirePlaceDescribtion
    serializer_class = FirePlaceDescribtionSerializer

    
class MapDescribtionView(BaseAPIView):
    model = MapDescribtion
    serializer_class = MapDescribtionSerializer


class IncidentByEvidenceAPIView(APIView):
    def get(self, request, evidence_id):
        # Get the evidence object or return 404
        evidence = get_object_or_404(Evidence, id=evidence_id)

        # Check if there is an incident linked to this evidence
        if not evidence.incident:
            return Response({"error": "No incident linked to this evidence"}, status=status.HTTP_404_NOT_FOUND)

        # Get incident details
        incident = evidence.incident
        data = {
            "investigative_body": incident.investigative_body,
            "inspection_date": incident.inspection_date.strftime("%Y-%m-%d"),
            "inspection_time": incident.inspection_time.strftime("%H:%M:%S"),
            "incident_location": incident.incident_location,
            "incident_date": incident.incident_date.strftime("%Y-%m-%d"),
            "description": incident.description,
            "procedure": incident.procedure,
        }

        return Response({"data" : data}, status=status.HTTP_200_OK)
class EvidenceByIncidentAPIView(APIView):
    def get(self, request, incident_id):
        # Fetch all Evidence related to the provided incident_id
        evidence_list = Evidence.objects.filter(incident_id=incident_id)
        
        # If no evidence is found, return a 404 error
        if not evidence_list:
            return Response({"detail": "No evidence found for this incident."}, status=status.HTTP_404_NOT_FOUND)
        
        # Serialize the Evidence data
        serializer = EvidenceSerializer(evidence_list, many=True)
        
        # Return the serialized data in the response
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
