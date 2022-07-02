from datetime import tzinfo
from django.db import models
from uuid import uuid4


# Create your models here.
class Aircraft(models.Model):
    serial_number = models.UUIDField(
        primary_key=True, unique=True, default=uuid4, editable=False
    )
    manufacturer = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ["-created_at"]



class AirPortInfo(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4, editable=False)
    icao = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    subd = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    elevation = models.FloatField(default=0.0)
    lat = models.FloatField(default=0.0)
    lon = models.FloatField(default=0.0)
    tz = models.CharField(max_length=255)


class ArrivalInfo(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4, editable=False)
    airport_info = models.ForeignKey(AirPortInfo, on_delete=models.CASCADE)
    estemated_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DepartureInfo(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4, editable=False)
    airport_info = models.ForeignKey(AirPortInfo, on_delete=models.CASCADE)
    estemated_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    


class Flight(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4, editable=False)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.SET_NULL, null=True)
    arrival_details = models.ForeignKey(ArrivalInfo, on_delete=models.SET_NULL, null=True)
    departure_details = models.ForeignKey(DepartureInfo, on_delete=models.SET_NULL, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ["-created_at"]
