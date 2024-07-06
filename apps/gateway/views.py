import traceback

from django.http import JsonResponse
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.gateway.serializers import GatewaySerializer,DeviceSerializer
from config.utils.utlis_view_api import CustomPagination

from ..users.authentication import IsTokenValid
from .models import Gateway,Device


# Create your views here.


class GatewayController(viewsets.ModelViewSet):
    serializer_class = GatewaySerializer
    pagination_class = CustomPagination
    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()

class DeviceController(viewsets.ModelViewSet):
    serializer_class = DeviceSerializer
    pagination_class = CustomPagination
    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()
