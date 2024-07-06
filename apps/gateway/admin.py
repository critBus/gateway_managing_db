from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Device,Gateway
# Register your models here.
@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    readonly_fields = ["date_created"]
    list_display = (
        "id",
        "vendor",
        "status",
        "date_created",
    )
    search_fields = (
        "id",
        "vendor",
        "status",
    )
    list_filter = (
        "status",
        "date_created",
    )
    ordering = (
        "-id",
        "vendor",
        "status",
        "date_created",
    )
    date_hierarchy = "date_created"
    list_display_links = list(list_display).copy()


@admin.register(Gateway)
class GatewayAdmin(admin.ModelAdmin):
    def devices(self, obj):
        nombres = [v.vendor for v in obj.device.all()]
        return mark_safe("<br>\n".join(nombres))
    list_display = (
        "id",
        "serial_number",
        "name",
        "ip_address",
        "devices"
    )
    search_fields = (
        "id",
        "serial_number",
        "name",
        "ip_address",
    )

    ordering = (
        "-id",
        "serial_number",
        "name",
        "ip_address",
    )
    list_display_links = list(list_display).copy()