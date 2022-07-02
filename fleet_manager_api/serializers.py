from rest_framework import serializers
from .models import AirPortInfo, ArrivalInfo, DepartureInfo, Flight, Aircraft
import airportsdata

airports = airportsdata.load()


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = "__all__"

    # def create(self, validated_data):
    #     arrival_airport = validated_data["arrival_airport"].upper()
    #     depature_airport = validated_data["depature_airport"].upper()
        
    #     if (arrival_airport in airports.keys()) and (
    #         depature_airport in airports.keys() and (
    #         arrival_airport != depature_airport  
    #         )
    #     ):
    #         flight = Flight.objects.create(**validated_data)
    #         flight.arrival_airport = validated_data["arrival_airport"].upper()
    #         flight.depature_airport = validated_data["depature_airport"].upper()
    #         flight.save()
    #         return flight


class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = "__all__"
        

class AirPortInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirPortInfo
        fields = "__all__"
        
    # def create(self, validated_data):
    #     # arrival_airport = validated_data["arrival_airport"].upper()
    #     # depature_airport = validated_data["depature_airport"].upper()
        
    #     # if (arrival_airport in airports.keys()) and (
    #     #     depature_airport in airports.keys() and (
    #     #     arrival_airport != depature_airport  
    #     #     )
    #     # ):
    #     airport = AirPortInfo.objects.create()
    #     flight.arrival_airport = validated_data["arrival_airport"].upper()
    #     flight.depature_airport = validated_data["depature_airport"].upper()
    #     flight.save()
    #     return flight


class ArrivalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArrivalInfo
        fields = "__all__"

class DepartureInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartureInfo
        fields = "__all__"       
        

class FlightScheduleSerializer(serializers.Serializer):
    departure_airport_icao = serializers.CharField(max_length=4)
    arrival_airport_icao = serializers.CharField(max_length=4)
    arrival_time = serializers.DateTimeField()
    departure_time = serializers.DateTimeField()
    
    
