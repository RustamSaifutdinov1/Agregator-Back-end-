from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .models import *


class ClinicsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Clinics
        fields = "__all__"


class DoctorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Doctor
        fields = "__all__"


class ServicesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Services
        fields = "__all__"


class CategoryClinicsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CategoryClinics
        fields = "__all__"
