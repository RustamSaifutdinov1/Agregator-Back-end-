from django.db import models


class Clinics(models.Model):
    ClinicName = models.CharField(max_length=50, blank=True)
    ClinicContent = models.TextField(blank=True)
    ClinicAddress = models.TextField(blank=True)
    ClinicTelephone = models.CharField(max_length=50, blank=True)
    ClinicTime_create = models.DateTimeField(auto_now_add=True)
    ClinicTime_update = models.DateTimeField(auto_now=True)
    ClinicIs_published = models.BooleanField(default=True)
    ClinicCat = models.ForeignKey('CategoryClinics', on_delete=models.PROTECT, null=True)
    ClinicPhoto = models.ImageField(upload_to='photos/%Y/%m/%d/')
    ClinicWork_time = models.TextField(blank=True)

    def __str__(self):
        return self.ClinicName


class CategoryClinics(models.Model):
    CategoryName = models.CharField(max_length=32, db_index=True)

    def __str__(self):
        return self.CategoryName


class Services(models.Model):
    ServiceName = models.CharField(max_length=50, blank=True)
    ServicePhoto = models.ImageField(upload_to='photos/%Y/%m/%d/')
    ServiceClinic = models.ForeignKey('Clinics', on_delete=models.PROTECT, null=True)
    ServicePrice = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.ServiceName


class Doctor(models.Model):
    DoctorClinic = models.ForeignKey('Clinics', on_delete=models.PROTECT, null=True)
    DoctorName = models.CharField(max_length=50, blank=True)
    DoctorContent = models.TextField(null=True)
    DoctorPhoto = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    DoctorIs_published = models.BooleanField(default=True)

    def __str__(self):
        return self.DoctorName


class Reviews(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=50)
    text = models.CharField(max_length=100)
    review_clinic = models.ForeignKey('Clinics', on_delete=models.PROTECT, null=True)
    rating = models.IntegerField()

    def __str__(self):
        return self.name
