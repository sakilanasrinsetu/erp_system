from django.shortcuts import render
from utils.custom_viewset import CustomViewSet

from utils.response_wrapper import ResponseWrapper
from dashboard.models import *
from dashboard.serializers import *

# Create your views here.

class CompanyViewSet(CustomViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    lookup_field = 'pk'