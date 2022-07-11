import re

from rest_framework import serializers

from .models import Aircraft, AirPortInfo, Flight


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = "__all__"


class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = "__all__"


class AirPortInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirPortInfo
        fields = "__all__"

    def create(self, validated_data):
        icaoRegex = re.compile(r"^\d{2}[A-Z]{2}$")
        validate_icao = icaoRegex.search(validated_data["icao"]) is None

        if validate_icao:
            raise ValueError(
                "Invalid depature icao must conatin two digits and two uppercase letters"
            )

        airport = AirPortInfo.objects.create(**validated_data)
        airport.save()
        return airport
