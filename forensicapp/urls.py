from django.urls import path
from .views import *
urlpatterns = [
    path('incidents/', IncindentView.as_view(), name='incident-list-create'),
    path('incidents/<int:pk>/', IncindentView.as_view(), name='incident-detail'),
    # retrieve all evidence
    path('evidence/', EvidenceView.as_view(), name='evidence-list-create'),
    # Retrieve, update, and delete a specific Evidence
    path('evidence/<int:pk>/', EvidenceView.as_view(), name='evidence-list-create'),
    # Retrieve, update, and delete a specific Incident
    path('complaint/<int:pk>/', ComplaintView.as_view(), name='incident-detail'),
    # Retrieve all procedures associated with a specific Incident
    path('complaint/', ComplaintView.as_view(), name='incidents'),
    path('inspection-form-details/', InspectionFormDetailsView.as_view(), name='inspection-form-details'),
    path('inspection-form-details/<int:pk>/', InspectionFormDetailsView.as_view(), name='inspection-form-details-detail'),
    path('inspection-form-labs/', InspectionFormLabsView.as_view(), name='inspection-form-labs'),
    path('inspection-form-labs/<int:pk>/', InspectionFormLabsView.as_view(), name='inspection-form-labs-detail'),
    path('fireplace/', FirePlaceDescribtionView.as_view()),
    path('fireplace/<int:pk>/', FirePlaceDescribtionView.as_view()),
    path('maps/' , MapDescribtionView.as_view()),
    path('map/<int:pk>/', MapDescribtionView.as_view()),
    # path('incident/evidence/<int:evidence_id>/', IncidentByEvidenceAPIView.as_view(), name='incident_by_evidence_api'),
    path('evidencebyincident/<int:incident_id>/', EvidenceByIncidentAPIView.as_view(), name='incident_details_api'),
        path('inspection-labs-by-incident/<int:incident_id>/', InspectionLabsByIncidentIdView.as_view(), name='inspection-labs-by-incident'),


]


