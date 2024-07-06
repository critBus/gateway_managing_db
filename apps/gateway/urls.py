from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import GatewayController,DeviceController

router = DefaultRouter()
app_name = "gateway"
router.register(r"gateway", GatewayController, basename="gateway")
router.register(r"device", GatewayController, basename="device")
urlpatterns = router.urls

