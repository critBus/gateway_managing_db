from rest_framework import serializers

from .models import Gateway,Device


class GatewaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gateway
        fields = "__all__"

class DeviceSerializer(serializers.ModelSerializer):
    device=GatewaySerializer(many=True)
    class Meta:
        model = Device
        fields = "__all__"