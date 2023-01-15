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
    
    # def cloud_cafe_information_details(self, request, *args, **kwargs):
    #     cloud_cafe_information_qs = CloudCafeInformation.objects.all().last()
    #     if not cloud_cafe_information_qs:
    #         return ResponseWrapper(error_msg='cloud cafe information Details Not Found', status=400)
    #     serializer = CloudCafeInformationSerializer(instance=cloud_cafe_information_qs)
    #     return ResponseWrapper(data=serializer.data, status=200)   
