from django.db import models
from django.utils import timezone

# Create your models here.
# محضر كشف واظهار الاثار الجرمية في مسرح الجريمة 

class Incident(models.Model):
    investigative_body = models.CharField(max_length=255 , default="")  # الجهة التحقيقية
    inspection_date =  models.DateField(default=timezone.now)  # تاريخ إجراء الكشف
    inspection_time = models.TimeField(default=timezone.now)  # وقت إجراء الكشف
    incident_location = models.CharField(max_length=500 , default="")  # عنوان محل الحادث
    incident_type= models.CharField(max_length=255 , default="") # نوع الحادث
    incident_date = models.DateField(default=timezone.now )  # تاريخ الحادث
    description = models.TextField(null=True , blank=True)  # وصف الحادث
    method = models.TextField(null=True , blank=True) # الطريقة
    procedure = models.TextField(null=True , blank=True) # الاجراءات المتخذة


    def __str__(self):
        return f"{self.investigative_body} - {self.incident_location}"
    
class Evidence(models.Model):
    number = models.IntegerField() # رقم الاثر 
    Typeofevidence = models.CharField(max_length=255 , default="") # نوع الاثر
    place = models.TextField(null=True , blank=True) # مكان الرفع
    waytosave = models.TextField(null=True , blank=True) # طريقة الرفع
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE , null=True)
    

    def __str__(self):
        return f"{self.number} - {self.Typeofevidence}"


class Complaint(models.Model):
    #  المشتكي
    name = models.CharField(max_length=255 , default="")
    action = models.TextField(null=True , blank=True)
    section_id = models.ForeignKey(Incident, on_delete=models.CASCADE , null=True)
    state = models.CharField(max_length=255 , default="")


    def __str__(self):
        return f"Complaint by {self.name}"    



# استمارة استلام و تسليم العينات

class InspectionFormDetails(models.Model):
    inspection_date = models.DateField(default=timezone.now)
    request_authority = models.CharField(max_length=255, default="")
    incident = models.TextField(null=True, blank=True)

    # ForeignKey to Incident (one-to-one relationship with Incident model)
    incident_obj = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name="inspection_details", null=True)

    def save(self, *args, **kwargs):
        # If we have a related Incident, set the fields accordingly
        if self.incident_obj:
            self.inspection_date = self.incident_obj.inspection_date
            self.request_authority = self.incident_obj.investigative_body
            self.incident = self.incident_obj.incident_type

        super(InspectionFormDetails, self).save(*args, **kwargs)

    def __str__(self):
        return f"Inspection Form Details for {self.incident_obj}"

class InspectionFormLabs(models.Model):
    # ForeignKey to title
    inspection_details = models.ForeignKey(InspectionFormDetails, on_delete=models.CASCADE, related_name="labs")

    #fields 
    evidence = models.ForeignKey(Evidence, on_delete=models.PROTECT, related_name='details', null=True, blank=True)
    count = models.IntegerField(default=1)
    crime_lab = models.BooleanField(default=False, verbose_name="مختبر الجريمة")
    weapon_lab = models.BooleanField(default=False, verbose_name="مختبر الأسلحة")
    chemistry_lab = models.BooleanField(default=False, verbose_name="مختبر الكيمياء")
    dna_lab = models.BooleanField(default=False, verbose_name="مختبر DNA")
    cyber_crime_lab = models.BooleanField(default=False, verbose_name="مختبر الجرائم الإلكترونية")

    def __str__(self):
        return f"Labs information for {self.inspection_details.incident_obj}"
    

# استمارة كشف الحرائق
class FirePlaceDescribtion(models.Model):
    inspection_time = models.TimeField(default=timezone.now)
    inspection_date = models.DateField(default=timezone.now)
    incident_date = models.DateField(default=timezone.now)
    request_authority = models.CharField(max_length=255 , default="")
    inspection_place = models.CharField(max_length=255 , default="")
    fire_place = models.TextField(null=True , blank=True)
    damage = models.TextField(null=True , blank=True)
    fire_reason = models.TextField(null=True , blank=True)
    procedures = models.TextField(null=True , blank=True)
    

# معلومات الخريطة 
class MapDescribtion(models.Model):
    title = models.CharField(max_length=255 , default="")
    color = models.CharField(max_length=255 , default="")
    description = models.TextField(null=True , blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.title
    