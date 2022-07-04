import airportsdata
from rest_framework import serializers

from .models import Aircraft, AirPortInfo, Flight

airports = airportsdata.load()


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
