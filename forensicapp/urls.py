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
    path('inspection-form/', InspectionFormView.as_view() , name='inspection-form'),  # لعرض جميع النماذج أو إضافة نموذج جديد
    path('inspection-form/<int:pk>/', InspectionFormView.as_view() , name='inspection-form-detail'),  # عرض، تعديل، أو حذف نموذج محدد
    path('fireplace/', FirePlaceDescribtionView.as_view()),
    path('fireplace/<int:pk>/', FirePlaceDescribtionView.as_view()),
    path('maps/' , MapDescribtionView.as_view()),
    path('map/<int:pk>/', MapDescribtionView.as_view()),
    # path('incident/evidence/<int:evidence_id>/', IncidentByEvidenceAPIView.as_view(), name='incident_by_evidence_api'),
    path('evidencebyincident/<int:incident_id>/', EvidenceByIncidentAPIView.as_view(), name='incident_details_api'),
    


]


