from django.db import models
from django.utils import timezone

# Create your models here.
# محضر كشف واظهار الاثلار الجرمية في مسرح الجريمة 

class Incident(models.Model):
    investigative_body = models.CharField(max_length=255 , default="")  # الجهة التحقيقية
    inspection_date =  models.DateField(default=timezone.now)  # تاريخ إجراء الكشف
    inspection_time = models.TimeField(default=timezone.now)  # وقت إجراء الكشف
    incident_location = models.CharField(max_length=500 , default="")  # عنوان محل الحادث
    incident_date = models.DateField(default=timezone.now )  # تاريخ الحادث
    description = models.TextField(null=True , blank=True)  # وصف الحادث
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

class InspectionForm(models.Model):
    # تاريخ الكشف
    inspection_date = models.DateTimeField(default=timezone.now)

    # جهة الطلب
    request_authority = models.CharField(max_length=255 , default="")

    # وصف الحادث
    incident_details = models.TextField(null=True , blank=True)
    # نوع الأثر - علاقة مع جدول Evidence
    evidence = models.ForeignKey(Evidence, on_delete=models.PROTECT, related_name='details' , null=True , blank=True) 
    # العدد
    count = models.IntegerField(default=1)
    # المختبرات
    crime_lab = models.BooleanField(default=False, verbose_name="مختبر الجريمة")
    weapon_lab = models.BooleanField(default=False, verbose_name="مختبر الأسلحة")
    chemistry_lab = models.BooleanField(default=False, verbose_name="مختبر الكيمياء")
    dna_lab = models.BooleanField(default=False, verbose_name="مختبر DNA")
    cyber_crime_lab = models.BooleanField(default=False, verbose_name="مختبر الجرائم الإلكترونية")



    def __str__(self):
        return f"Details for {self.evidence} - Count: {self.count}"
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
    