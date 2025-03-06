from django.shortcuts import render
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from .pagination import CustomPaginationWithResult
from django.shortcuts import get_object_or_404
from django.db.models import Q , Count
from rest_framework import filters
from .filters import IncidentFilter,InspectionFilter, FireFormFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter




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
    # Check if the request data is a list of items
        if isinstance(request.data, list):
            # If it's a list
            serializer = self.serializer_class(data=request.data, many=True)
        else:
            # If it's a single
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

    def delete(self, request, pk=None):
        if pk:
            # Delete a single instance
            try:
                instance = self.model.objects.get(pk=pk)
                instance.delete()
                return Response({'message': 'Deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
            except self.model.DoesNotExist:
                return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Delete all instances if no pk is provided
            self.model.objects.all().delete()
            return Response({'message': 'All data deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

class IncindentView(BaseAPIView):
    model = Incident
    serializer_class = IncidentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = IncidentFilter
    ordering_fields = ['id', 'inspection_date']
    ordering = ['-id']  # Default ordering

    def get(self, request, pk=None):
        if pk:
            # Retrieve a single incident by primary key (pk)
            incident = get_object_or_404(self.model, pk=pk)
            serializer = self.serializer_class(incident)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        
        # Retrieve all incidents with optional filtering
        queryset = self.model.objects.all()

        # Apply filters if any are present in the request
        filtered_queryset = self.filterset_class(request.GET, queryset=queryset).qs

        # Apply ordering if specified in the request
        ordering = request.GET.get('ordering', '-id')  # Default ordering is descending by id
        filtered_queryset = filtered_queryset.order_by(ordering)

        # Paginate the filtered and ordered queryset
        paginator = CustomPaginationWithResult()
        result_page = paginator.paginate_queryset(filtered_queryset, request)
        serializer = self.serializer_class(result_page, many=True)

        # Return paginated response
        return paginator.get_paginated_response(serializer.data)

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
    ordering_fields = ['id' , 'inspection_date' ]
    ordering = ['-id']
    def get(self, request, pk=None):
        """
        GET request to retrieve all InspectionForms or a single form by pk.
        """
        if pk:
            # Retrieve a single inspection form by primary key (pk)
            inspection_form = get_object_or_404(self.model, pk=pk)
            serializer = self.serializer_class(inspection_form)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)

        # Retrieve all with filtering and ordering
        queryset = self.model.objects.all()
        # Apply filters if any are present in the request

        filtered_queryset = self.filterset_class(request.GET, queryset=queryset).qs 
        # Apply ordering 
        ordering = request.GET.get('ordering', '-id') 
        filtered_queryset = filtered_queryset.order_by(ordering)
        paginator = CustomPaginationWithResult()
        result_page = paginator.paginate_queryset(filtered_queryset, request)

        serializer = self.serializer_class(result_page, many=True)

        # Return paginated response
        return paginator.get_paginated_response(serializer.data)


class FirePlaceDescribtionView(BaseAPIView):
    model = FirePlaceDescribtion
    serializer_class = FirePlaceDescribtionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = FireFormFilter
    ordering_fields = ['id' , 'inspection_date' , 'incident_date' ]
    ordering = ['-id']
    def get(self, request, pk=None):
        """
        GET request to retrieve all InspectionForms or a single form by pk.
        """
        if pk:
            # Retrieve a single inspection form by primary key (pk)
            FireForm = get_object_or_404(self.model, pk=pk)
            serializer = self.serializer_class(FireForm)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)

        # Retrieve all with filtering and ordering
        queryset = self.model.objects.all()
        # Apply filters if any are present in the request

        filtered_queryset = self.filterset_class(request.GET, queryset=queryset).qs 
        # Apply ordering 
        ordering = request.GET.get('ordering', '-id') 
        filtered_queryset = filtered_queryset.order_by(ordering)
        paginator = CustomPaginationWithResult()
        result_page = paginator.paginate_queryset(filtered_queryset, request)

        serializer = self.serializer_class(result_page, many=True)

        # Return paginated response
        return paginator.get_paginated_response(serializer.data)

    
class MapDescribtionView(BaseAPIView):
    model = MapDescribtion
    serializer_class = MapDescribtionSerializer


# class IncidentByEvidenceAPIView(APIView):
#     def get(self, request, evidence_id):
#         # Get the evidence object or return 404
#         evidence = get_object_or_404(Evidence, id=evidence_id)

#         # Check if there is an incident linked to this evidence
#         if not evidence.incident:
#             return Response({"error": "No incident linked to this evidence"}, status=status.HTTP_404_NOT_FOUND)

#         # Get incident details
#         incident = evidence.incident
#         data = {
#             "investigative_body": incident.investigative_body,
#             "inspection_date": incident.inspection_date.strftime("%Y-%m-%d"),
#             "inspection_time": incident.inspection_time.strftime("%H:%M:%S"),
#             "incident_location": incident.incident_location,
#             "incident_date": incident.incident_date.strftime("%Y-%m-%d"),
#             "description": incident.description,
#             "procedure": incident.procedure,
#         }

#         return Response({"data" : data}, status=status.HTTP_200_OK)
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


class InspectionLabsByIncidentIdView(APIView):
    def get(self, request, incident_id):
        """
        GET request to retrieve all InspectionForm in a specific incident_id,
        """
        # Fetch all InspectionForm records related to the provided incident_id
        inspection_forms = InspectionForm.objects.filter(incident_obj__id=incident_id)

        if not inspection_forms.exists():
            return Response({"detail": "No inspection forms found for this incident."}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the data
        serializer = InspectionFormSerializer(inspection_forms, many=True)

        # Remove specific fields from the response
        customized_data = [
            {
                "id": item["id"],
                "count": item["count"],
                "crime_lab": item["crime_lab"],
                "weapon_lab": item["weapon_lab"],
                "chemistry_lab": item["chemistry_lab"],
                "dna_lab": item["dna_lab"],
                "cyber_crime_lab": item["cyber_crime_lab"],
                "evidence": item["evidence"],
                "incident_obj": item["incident_obj"]
            }
            for item in serializer.data
        ]

        return Response({"data": customized_data}, status=status.HTTP_200_OK)




class IncidentStatisticsView(APIView):
    def get(self, request):
        # Apply filters manually
        filterset = IncidentFilter(request.GET, queryset=Incident.objects.all())

        if not filterset.is_valid():
            return Response({"error": "Invalid filters"}, status=400)

        # Apply filtering, then group by 'incident_type' and count
        filtered_incidents = filterset.qs
        stats = filtered_incidents.values('incident_type').annotate(count=Count('id'))

        serializer = IncidentStatisticsSerializer(stats, many=True)
        return Response(serializer.data)