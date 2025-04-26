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
from uuid import UUID
from rest_framework.exceptions import NotFound

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
                return Response(
                    {
                        "error": f"{self.model.__name__} with ID {pk} was not found.",
                        "status_code": status.HTTP_404_NOT_FOUND
                    },     status=status.HTTP_404_NOT_FOUND
                )
        try:
            paginator = CustomPaginationWithResult()
            instances = self.model.objects.all().order_by('-id')
            result_page = paginator.paginate_queryset(instances, request)
            serializer = self.serializer_class(result_page, many=True)
            logger.info(f"Retrieved list of {self.model.__name__}")
            return paginator.get_paginated_response(serializer.data)


        except:
            logger.error(f"Failed to retrieve list of {self.model.__name__}. No records found.")
            return Response(
                {
                    "error": f"No {self.model.__name__} records found.",
                    "status_code": status.HTTP_404_NOT_FOUND
                }, 
                status=status.HTTP_404_NOT_FOUND
            )



    def post(self, request):
    # Check if the request data is a list
        is_bulk_create = isinstance(request.data, list)

        try:
            serializer = self.serializer_class(data=request.data, many=is_bulk_create)
        except Exception as e:
            logger.error(f"Error initializing serializer for {self.model.__name__}: {e}")
            return Response(
                {
                    "error": f"Failed to process {self.model.__name__} data.",
                    "details": str(e),
                    "status_code": status.HTTP_400_BAD_REQUEST
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )

        if serializer.is_valid():
            try:
                serializer.save()
                logger.info(f"Successfully created {self.model.__name__} instance(s)")
                return Response({"data": serializer.data})
            except Exception as e:
                logger.error(f"Failed to create {self.model.__name__} instance(s): {e}")
                return Response(
                    {
                        "error": f"Failed to create {self.model.__name__} instance(s).",
                        "details": str(e),
                        "status_code": status.HTTP_400_BAD_REQUEST
                    }, 
                    status=status.HTTP_400_BAD_REQUEST
                )

        # If serializer is not valid, return validation errors
        logger.error(f"Invalid data provided for {self.model.__name__}: {serializer.errors}")
        return Response(
            {
                "error": "Invalid data.",
                "validation_errors": serializer.errors,
                "status_code": status.HTTP_400_BAD_REQUEST
            }, 
            status=status.HTTP_400_BAD_REQUEST
        )


    def put(self, request, pk):
        try:
            instance = self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            logger.error(f"{self.model.__name__} with ID {pk} not found.")
            return Response(
                {
                    "error": f"{self.model.__name__} with ID {pk} not found.",
                    "status_code": status.HTTP_404_NOT_FOUND
                },
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            serializer = self.serializer_class(instance, data=request.data, partial=True)  # Allow partial updates
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Successfully updated {self.model.__name__} with ID {pk}.")
                return Response({"data": serializer.data})
            else:
                logger.error(f"Validation failed for updating {self.model.__name__} with ID {pk}: {serializer.errors}")
                return Response(
                    {
                        "error": "Invalid data provided.",
                        "validation_errors": serializer.errors,
                        "status_code": status.HTTP_400_BAD_REQUEST
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            logger.error(f"Failed to update {self.model.__name__} with ID {pk}: {str(e)}")
            return Response(
                {
                    "error": f"Failed to update {self.model.__name__}.",
                    "details": str(e),
                    "status_code": status.HTTP_400_BAD_REQUEST
                },
                status=status.HTTP_400_BAD_REQUEST
            )


    def delete(self, request, pk=None):
        try:
            if pk:
                # Delete a single instance
                try:
                    instance = self.model.objects.get(pk=pk)
                    instance.delete()
                    logger.info(f"Deleted {self.model.__name__} with ID {pk}.")
                    return Response(
                        {
                            "message": f"{self.model.__name__} with ID {pk} deleted successfully.",
                            "status_code": status.HTTP_204_NO_CONTENT
                        },
                        status=status.HTTP_204_NO_CONTENT
                    )
                except self.model.DoesNotExist:
                    logger.error(f"{self.model.__name__} with ID {pk} not found.")
                    return Response(
                        {
                            "error": f"{self.model.__name__} with ID {pk} not found.",
                            "status_code": status.HTTP_404_NOT_FOUND
                        },
                        status=status.HTTP_404_NOT_FOUND
                    )

            # Delete all instances if no pk is provided (Bulk delete)
            queryset = self.model.objects.all()
            if not queryset.exists():
                logger.error(f"No {self.model.__name__} instances found to delete.")
                return Response(
                    {
                        "error": f"No {self.model.__name__} instances found to delete.",
                        "status_code": status.HTTP_404_NOT_FOUND
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            deleted_count, _ = queryset.delete()
            logger.info(f"Deleted {deleted_count} {self.model.__name__} instances.")
            return Response(
                {
                    "message": f"Deleted {deleted_count} {self.model.__name__} instances successfully.",
                    "status_code": status.HTTP_204_NO_CONTENT
                },
                status=status.HTTP_204_NO_CONTENT
            )

        except Exception as e:
            logger.error(f"Failed to delete {self.model.__name__}: {str(e)}")
            return Response(
                {
                    "error": f"An error occurred while deleting {self.model.__name__}.",
                    "details": str(e),
                    "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class IncindentView(BaseAPIView):
    model = Incident
    serializer_class = IncidentSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = IncidentFilter
    ordering_fields = ['id', 'inspection_date']
    ordering = ['-id']  # Default ordering

    def get(self, request, uuid=None):
        try:
            if uuid:
                # Retrieve a single instance by primary key (pk)
                incident = get_object_or_404(self.model, uuid=uuid)
                serializer = self.serializer_class(incident)
                logger.info(f"Retrieved {self.model.__name__} with ID {uuid}.")
                return Response({"data" : serializer.data})

            # Retrieve all instances with optional filtering
            queryset = self.model.objects.all()

            # Apply filters if filterset_class is defined
            if hasattr(self, 'filterset_class') and self.filterset_class:
                queryset = self.filterset_class(request.GET, queryset=queryset).qs

            # Apply ordering if specified in the request
            ordering = request.GET.get('ordering', '-id')
            valid_ordering_fields = [field.name for field in self.model._meta.fields]

            # Ensure ordering field is valid
            if ordering.lstrip('-') in valid_ordering_fields:
                queryset = queryset.order_by(ordering)
            else:
                logger.error(f"Invalid ordering field: {ordering}. Using default ordering.")
                queryset = queryset.order_by('-id')

            # Paginate the filtered and ordered queryset
            paginator = CustomPaginationWithResult()
            result_page = paginator.paginate_queryset(queryset, request)
            serializer = self.serializer_class(result_page, many=True)

            # Return paginated response
            logger.info(f"Retrieved {len(serializer.data)} {self.model.__name__} instances.")
            return paginator.get_paginated_response(serializer.data)

        except self.model.DoesNotExist:
            logger.error(f"{self.model.__name__} with ID {uuid} not found.")
            return Response(
                {"error": f"{self.model.__name__} with ID {uuid} not found.", "status_code": status.HTTP_404_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            logger.error(f"Failed to retrieve {self.model.__name__}: {str(e)}")
            return Response(
                {"error": "An error occurred while retrieving data.", "details": str(e), "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    def put(self, request, uuid):
            try:
                instance = self.model.objects.get(uuid=uuid)
            except self.model.DoesNotExist:
                logger.error(f"{self.model.__name__} with UUID {uuid} not found.")
                return Response(
                    {
                        "error": f"{self.model.__name__} with UUID {uuid} not found.",
                        "status_code": status.HTTP_404_NOT_FOUND
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            try:
                serializer = self.serializer_class(instance, data=request.data, partial=True)  # Allow partial updates
                if serializer.is_valid():
                    serializer.save()
                    logger.info(f"Successfully updated {self.model.__name__} with UUID {uuid}.")
                    return Response({"data": serializer.data})
                else:
                    logger.error(f"Validation failed for updating {self.model.__name__} with UUID {uuid}: {serializer.errors}")
                    return Response(
                        {
                            "error": "Invalid data provided.",
                            "validation_errors": serializer.errors,
                            "status_code": status.HTTP_400_BAD_REQUEST
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except Exception as e:
                logger.error(f"Failed to update {self.model.__name__} with UUID {uuid}: {str(e)}")
                return Response(
                    {
                        "error": f"Failed to update {self.model.__name__}.",
                        "details": str(e),
                        "status_code": status.HTTP_400_BAD_REQUEST
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )






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
            inspection_form = self.model.objects.get(pk=pk)
            serializer = self.serializer_class(inspection_form)
            logger.info(f"Successfully retrieved {self.model.__name__} with id {pk}")

            return Response(
                {"data": serializer.data},
                status=status.HTTP_200_OK
            )
        except self.model.DoesNotExist:
            logger.error(f"{self.model.__name__} with ID {pk} not found.")
            return Response(
                {"error": f"{self.model.__name__} with ID {pk} not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error retrieving {self.model.__name__} with ID {pk}: {str(e)}")
            return Response(
                {"error": "An unexpected error occurred.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    try:
        # Retrieve all records with optional filtering and ordering
        queryset = self.model.objects.all()

        # Apply filters if filterset_class is defined
        if hasattr(self, 'filterset_class') and self.filterset_class:
            queryset = self.filterset_class(request.GET, queryset=queryset).qs 

        # Apply ordering safely
        ordering = request.GET.get('ordering', '-id') 
        if ordering.lstrip('-') in [field.name for field in self.model._meta.fields]:
            queryset = queryset.order_by(ordering)
        else:
            logger.error(f"Invalid ordering field: {ordering}. Defaulting to '-id'")
            queryset = queryset.order_by('-id')

        # Paginate the filtered and ordered queryset
        paginator = CustomPaginationWithResult()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(result_page, many=True)

        logger.info(f"Retrieved list of {self.model.__name__} ({queryset.count()} records)")

        # Return paginated response
        return paginator.get_paginated_response(serializer.data)

    except Exception as e:
        logger.error(f"Error retrieving list of {self.model.__name__}: {str(e)}")
        return Response(
            {"error": "An unexpected error occurred while retrieving the records.", "details": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )



class InspectionLabsByIncidentIdView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, form_uuid):
        """
        GET request to retrieve all InspectionForm records for a specific incident_id.
        """
        try:
            # Fetch all related InspectionForm records
            inspection_forms = InspectionForm.objects.filter(form_uuid=form_uuid)

            if not inspection_forms.exists():
                logger.error(f"No inspection forms found for incident_id: {form_uuid}")
                return Response({"detail": "No inspection forms found for this incident."}, status=status.HTTP_404_NOT_FOUND)

            # Serialize the data
            serializer = InspectionFormSerializer(inspection_forms, many=True)

            return Response({"data": serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error retrieving inspection forms for incident_id {form_uuid}: {str(e)}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class EvidenceByIncidentIdView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, incident_uuid):
        """
        GET request to retrieve all Evidence related to a specific incident_uuid.
        """
        try:
            # Fetch all Evidence records related to the given accident_uuid
            evidences = Evidence.objects.filter(accident_uuid=incident_uuid)

            if not evidences.exists():
                logger.error(f"No evidence found for accident_uuid: {incident_uuid}")
                return Response({"detail": "No evidence found for this incident."}, status=status.HTTP_404_NOT_FOUND)

            # Serialize the data
            serializer = EvidenceSerializer(evidences, many=True)

            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error retrieving evidence for accident_uuid {incident_uuid}: {str(e)}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class IncidentStatisticsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Apply filters manually
        filterset = IncidentFilter(request.GET, queryset=Incident.objects.all())

        if not filterset.is_valid():
            return Response({"error": "Invalid filters"}, status=400)

        # Apply filtering
        filtered_incidents = filterset.qs

        # Count by 'incident_type' (if exists) and 'category_accident'
        type_stats = filtered_incidents.values('typeAccident').annotate(count=Count('id'))
        category_stats = filtered_incidents.values('category_accident').annotate(count=Count('id'))

        return Response({
            "incident_type_counts": type_stats,
            "category_accident_counts": category_stats
        })
