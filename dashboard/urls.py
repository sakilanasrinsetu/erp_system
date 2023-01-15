from django.urls import include, path
from .views import *

urlpatterns = [
    path("company/",
         CompanyViewSet.as_view({'get': 'list', "post": "create"}), name="company"),
    path("company/<int:pk>/",
         CompanyViewSet.as_view({"patch": "update", "delete": "destroy", "get": "retive"}), name="company"),
]