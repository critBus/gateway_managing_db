from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator

# Create your models here.
def validate_noVacio(value):
    if len(str(value).strip()) == 0:
        raise ValidationError("Este campo no puede estar vacío.")




class Device(models.Model):
    class Meta:
        verbose_name = "Device"
        verbose_name_plural = "Devices"

    vendor= models.CharField(verbose_name="Name", max_length=256,)
    status=models.CharField(verbose_name="Name", max_length=256,choices=[("online","online"),("offline","offline")])
    date_created = models.DateTimeField(verbose_name="Date Created",auto_now_add=True)

class Gateway(models.Model):
    class Meta:
        verbose_name = "Gateway"
        verbose_name_plural = "Gateways"

    serial_number=models.CharField(verbose_name="Serial Number",max_length=256,unique=True)
    name = models.CharField(verbose_name="Name", max_length=256,)
    ip_address=models.GenericIPAddressField(verbose_name="Ip Address")
    device = models.ManyToManyField(Device)