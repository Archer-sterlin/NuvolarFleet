from uuid import uuid4

from django.db import models


class Aircraft(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4, editable=False)
    serial_number = models.CharField(max_length=255, unique=True)
    manufacturer = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.serial_number} - {self.manufacturer}"


class AirPortInfo(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4, editable=False)
    icao = models.CharField(max_length=4, unique=True)
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    subd = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255)
    elevation = models.FloatField(default=0.0, null=True, blank=True)
    lat = models.FloatField(default=0.0, null=True, blank=True)
    lon = models.FloatField(default=0.0, null=True, blank=True)
    tz = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.icao} - {self.name}"


class Flight(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4, editable=False)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.SET_NULL, blank=True, null=True)
    departure_airport = models.CharField(max_length=4)
    arrival_airport = models.CharField(max_length=4)
    departure = models.DateTimeField()
    arrival = models.DateTimeField()

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ["-created_at"]
