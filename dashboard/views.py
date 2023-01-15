from django.shortcuts import render
from utils.custom_viewset import CustomViewSet

from utils.response_wrapper import ResponseWrapper
from .models import *
from .serializers import *

# Create your views here.

class CompanyViewSet(CustomViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    lookup_field = 'pk'


class DepartmentViewSet(CustomViewSet):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()
    lookup_field = 'pk'
