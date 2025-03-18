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
from .filters import IncidentFilter,InspectionFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
import logging
logger = logging.getLogger('forensicapp')


class BaseAPIView(APIView):
    model = None
    serializer_class = None
    permission_classes = [AllowAny]


    def get(self, request, pk=None):
        if pk:
            try:
                instance = self.model.objects.get(pk=pk)
                serializer = self.serializer_class(instance)
                logger.info(f"Retrieved {self.model.__name__} with id {pk}")

                return Response({"data": serializer.data})
            except self.model.DoesNotExist:
                logger.error(f"{self.model.__name__} with id {pk} not found")
                return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            paginator = CustomPaginationWithResult()
            instances = self.model.objects.all().order_by('-id')
            result_page = paginator.paginate_queryset(instances, request)
            serializer = self.serializer_class(result_page, many=True)
            logger.info(f"Retrieved list of {self.model.__name__}")
            return paginator.get_paginated_response({"data": serializer.data})


        except:
                logger.error(f"Failed to retrieve list of {self.model.__name__}")
                return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)


    def post(self, request):
    # Check if the request data is a list of items
        if isinstance(request.data, list):
            # If it's a list
            try:
                serializer = self.serializer_class(data=request.data, many=True)
            except Exception as e:
                logger.error(f"Failed to retrieve list of {self.model.__name__}: {e}")
                return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                serializer = self.serializer_class(data=request.data)
            except Exception as e:
                logger.error(f"Failed to retrieve single {self.model.__name__}: {e}")
                return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            try:
                serializer.save()
                logger.info(f"Created new {self.model.__name__} instance(s)")

                return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error(f"Failed to create new {self.model.__name__} instance(s): {e}")
                return Response({'error': 'Failed to create new instance(s)'}, status=status.HTTP_400_BAD_REQUEST)

        # If serializer is not valid, log and return the errors
        logger.error(f"Invalid data provided: {serializer.errors}")
        return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, pk):
        try:
            instance = self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            logger.error(f"{self.model.__name__} with id {pk} not found")
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        

        try:
            serializer = self.serializer_class(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Updated {self.model.__name__} with id {pk}")
                return Response({"data": serializer.data})
        except:
            logger.error(f"Failed to update {self.model.__name__} with id {pk}")
            return Response({'error': 'Failed to update instance'}, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, pk=None):
        if pk:
            # Delete a single instance
            try:
                instance = self.model.objects.get(pk=pk)
                instance.delete()
                logger.info(f"Deleted {self.model.__name__} with id {pk}")
                return Response({'message': 'Deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
            except self.model.DoesNotExist:
                logger.error(f"{self.model.__name__} with id {pk} not found")
                return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Delete all instances if no pk is provided
            try:
                self.model.objects.all().delete()
                logger.info(f"Deleted all {self.model.__name__} instances")
                return Response({'message': 'Deleted all successfully'}, status=status.HTTP_204_NO_CONTENT)
            
            except:
                logger.error(f"{self.model.__name__} instances not found")
                return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

class IncindentView(BaseAPIView):
    model = Incident
    serializer_class = IncidentSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = IncidentFilter
    ordering_fields = ['id', 'inspection_date']
    ordering = ['-id']  # Default ordering

    def get(self, request, pk=None):
        if pk:
            try:
            # Retrieve a single incident by primary key (pk)
                incident = get_object_or_404(self.model, pk=pk)
                serializer = self.serializer_class(incident)
                logger.info(f"Retrieved {self.model.__name__} with id {pk}")
                return Response({"data": serializer.data}, status=status.HTTP_200_OK)
            except:
                logger.error(f"Failed to retrieve {self.model.__name__} with id {pk}")
                return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        

        try:
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
            logger.info(f"Retrieved list of {self.model.__name__}")
            return paginator.get_paginated_response(serializer.data)
        except:
            logger.error(f"Failed to retrieve list of {self.model.__name__}")
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

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
            try:
            # Retrieve a single inspection form by primary key (pk)
                inspection_form = self.model.objects.get(self.model, pk=pk)
                serializer = self.serializer_class(inspection_form)
                logger.info(f"Retrieved {self.model.__name__} with id {pk}")
                return Response({"data": serializer.data}, status=status.HTTP_200_OK)
            except:
                logger.error(f"Failed to retrieve {self.model.__name__} with id {pk}")
                return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
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
            logger.info(f"Retrieved list of {self.model.__name__}")

        # Return paginated response

            return paginator.get_paginated_response(serializer.data)
        except:
            logger.error(f"Failed to retrieve list of {self.model.__name__}")
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)



class InspectionLabsByIncidentIdView(APIView):
    permission_classes = [AllowAny]
    

    def get(self, request, incident_id):
        """
        GET request to retrieve all InspectionForm in a specific incident_id.
        """
        try:
            # Fetch all related InspectionForm records
            inspection_forms = InspectionForm.objects.filter(form_id=incident_id)

            if not inspection_forms.exists():
                logger.warning(f"No inspection forms found for incident_id: {incident_id}")
                return Response({"detail": "No inspection forms found for this incident."}, status=status.HTTP_404_NOT_FOUND)

            # Serialize the data
            serializer = InspectionFormSerializer(inspection_forms, many=True)

            # Customize response data
            customized_data = [
                {
                    "id": item.get("id"),
                    "uuid": item.get("uuid"),
                    "status": item.get("status"),
                    "user": item.get("user"),
                    "chemistry_lab": item.get("is_chemistry_lab"),
                    "weapons_lab": item.get("is_weapons_lab"),
                    "forensic_lab": item.get("is_forensic_lab"),
                    "criminal_print_lab": item.get("is_criminal_print"),
                    "dna_lab": item.get("is_dna_lab"),
                    "cyber_crime_lab": item.get("is_criminal_electronic"),
                    "incident_obj": item.get("form"),
                    "created_at": item.get("created_at"),
                    "updated_at": item.get("updated_at")
                }
                for item in serializer.data
            ]

            return Response({"data": customized_data}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error retrieving inspection forms for incident_id {incident_id}: {str(e)}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EvidenceByIncidentIdView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, incident_id):
        """
        GET request to retrieve all Evidence related to a specific incident_id.
        """
        try:
            # Fetch all Evidence records related to the given incident_id
            evidences = Evidence.objects.filter(accident_id=incident_id)

            if not evidences.exists():
                logger.warning(f"No evidence found for incident_id: {incident_id}")
                return Response({"detail": "No evidence found for this incident."}, status=status.HTTP_404_NOT_FOUND)

            # Serialize the data
            serializer = EvidenceSerializer(evidences, many=True)

            return Response({"data": serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error retrieving evidence for incident_id {incident_id}: {str(e)}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
    
