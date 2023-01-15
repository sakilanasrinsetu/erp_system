from rest_framework import serializers
from .models import *

class CompanySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Company
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Department
        fields = '__all__'