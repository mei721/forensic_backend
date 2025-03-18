from django.db import models
from django.utils import timezone
from accounts.models import CustomUser
# Create your models here.

# محضر كشف واظهار الاثار الجرمية في مسرح الجريمة 

class Incident(models.Model):
    uuid = models.CharField(max_length=36, unique=True  , blank= True)  # Assuming UUID is in string format
    date_discovery = models.TextField(default="" , null=True, blank=True)
    accident_date = models.TextField(default="" ,null=True, blank=True)
    investigating_body = models.CharField(max_length=255, default="")
    accident_description = models.TextField(default="")
    inspection_time = models.TextField(null=True, blank=True)
    accident_location = models.CharField(max_length=255, null=True, blank=True)
    action_taken = models.TextField(null=True, blank=True)
    method = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=50, default='local')
    latitude = models.CharField(max_length=50, null=True, blank=True)
    longitude = models.CharField(max_length=50, null=True, blank=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    typeAccident = models.CharField(max_length=100, null=True, blank=True)
    resulting_damages = models.TextField(null=True, blank=True)
    causes_of_fire = models.TextField(null=True, blank=True)
    category_accident = models.CharField(
        max_length=20,
        choices=[('fireAccident', 'Fire Accident'), ('accident', 'Accident')],
        default='accident'
    )
    user = models.ForeignKey(CustomUser, related_name='accidents', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Accident {self.uuid} - {self.status}"

# الاثار الجرمية
    
class Evidence(models.Model):
        uuid = models.CharField(max_length=255, unique=True, blank=True, null=True)
        accident_Id = models.ForeignKey('Incident', on_delete=models.CASCADE, related_name='evidences' , null=True, blank=True)
        sampleType = models.CharField(max_length=255, null=True, blank=True)
        sampleNumber = models.CharField(max_length=255, null=True, blank=True)
        Placeoflifting = models.CharField(max_length=255, null=True, blank=True)
        metodeIifting = models.CharField(max_length=255, null=True, blank=True)
        status = models.CharField(max_length=50, default='local')
        userId = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
        created_at = models.DateTimeField(default=timezone.now)
        updated_at = models.DateTimeField(auto_now=True)
        def __str__(self):
            return f"AccidentSample {self.id} - {self.sample_type} ({self.status})"

# لجنة الشكاوي
class Complaint(models.Model):
    uuid = models.CharField(max_length=255, unique=True, blank=True, null=True)
    section = models.ForeignKey('Incident', on_delete=models.CASCADE, related_name='sections' , null=True, blank=True)
    name = models.CharField(max_length=255)
    action = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, default='local')
    userId = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    isHidden  = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Accident Section {self.id} - {self.name} ({self.status})"



# استمارة استلام و تسليم العينات

class InspectionForm(models.Model):
    uuid = models.CharField(max_length=255, unique=True, blank=True, null=True)
    form_id = models.ForeignKey('Incident', on_delete=models.CASCADE, related_name='inspection_forms' , null=True, blank=True)
    isChemistryLab = models.BooleanField(default=False)
    isWeaponsLab = models.BooleanField(default=False)
    isForensicLab = models.BooleanField(default=False)
    isCriminalPrint = models.BooleanField(default=False)
    isDNALab = models.BooleanField(default=False)
    isCriminalElectronic = models.BooleanField(default=False)
    status = models.CharField(max_length=50, default='local')
    userId = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"SampleDetail {self.id} - Status: {self.status}"



# استمارة كشف الحرائق
# class FirePlaceDescribtion(models.Model):
#     inspection_time = models.TextField(default='',null=True, verbose_name="الوقت")
#     inspection_date = models.DateField(default=timezone.now)
#     incident_date = models.DateField(default=timezone.now)
#     request_authority = models.CharField(max_length=255 , default="")
#     inspection_place = models.CharField(max_length=255 , default="")
#     fire_place = models.TextField(null=True , blank=True)
#     damage = models.TextField(null=True , blank=True)
#     fire_reason = models.TextField(null=True , blank=True)
#     procedures = models.TextField(null=True , blank=True)
    
# class FireEvidence(models.Model):
#     number = models.IntegerField( verbose_name="رقم الاثر") # رقم الاثر 
#     Typeofevidence = models.CharField(max_length=255 , default="" , verbose_name="نوع الاثر") # نوع الاثر
#     place = models.TextField(null=True , blank=True , verbose_name="مكان الرفع" ) # مكان الرفع
#     waytosave = models.TextField(null=True , blank=True, verbose_name="طريقة الرفع") # طريقة الرفع
#     fire_incident = models.ForeignKey(FirePlaceDescribtion, on_delete=models.CASCADE , null=True , verbose_name="الحادث")
    

#     def __str__(self):
#         return f"{self.number} - {self.Typeofevidence}"

# معلومات الخريطة 
# class MapDescribtion(models.Model):
#     title = models.CharField(max_length=255 , default="")
#     color = models.CharField(max_length=255 , default="")
#     description = models.TextField(null=True , blank=True)
#     latitude = models.FloatField()
#     longitude = models.FloatField()

#     def __str__(self):
#         return self.title