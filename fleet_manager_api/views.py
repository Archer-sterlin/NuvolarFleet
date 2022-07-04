from datetime import datetime 
from django.utils import timezone
from rest_framework import generics, response, status
from .serializers import (
    AirPortInfoSerializer,
    FlightSerializer,
    AircraftSerializer,
)
from .models import AirPortInfo, Flight, Aircraft


now = timezone.now()

class AirCraftView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AircraftSerializer
    queryset = Aircraft.objects.all()

class ListAirCraftView(generics.ListCreateAPIView):
    serializer_class = AircraftSerializer
    queryset = Aircraft.objects.all()

class AirportInfoView(generics.ListCreateAPIView):
    serializer_class = AirPortInfoSerializer
    queryset = AirPortInfo.objects.all()[:10]

class EditAirportInfoView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AirPortInfoSerializer
    queryset = AirPortInfo.objects.all()[:10]


class DepartureFlightsView(generics.ListAPIView):
    serializer_class = FlightSerializer
    def get_queryset(self):
        return Flight.objects.filter(departure_airport=self.kwargs["icao"])


class ArrivalFlightsView(generics.ListAPIView):
    serializer_class = FlightSerializer
    def get_queryset(self):
        return Flight.objects.filter(arrival_airport=self.kwargs["icao"])
    
class FlightScheduleView(generics.ListCreateAPIView):
    serializer_class = FlightSerializer
    queryset = Flight.objects.all()     
    
class EditFlightScheduleView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FlightSerializer
    queryset = Flight.objects.all() 
    
    def post(self, request, *args, **kwargs):
        try: 
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                airport = AirPortInfo.objects.all()[:]
                icao_arrival = serializer.validated_data["arrival_airport"].upper()
                icao_departure = serializer.validated_data["departure_airport"].upper()
                arrival_airport = airport.get(icao=icao_arrival)
                arrival = serializer.validated_data["arrival"]
                departure = serializer.validated_data["departure"]
                departure_airport = airport.get(icao=icao_arrival)
                aircraft = serializer.validated_data["aircaft"]
                
                if arrival == departure:
                         raise Exception("arrival airport cannot be the same as departure airport")
                
                if  (arrival < departure) and (departure >= now):
                    raise Exception("Invalid date, make sure dates are future date and arrival date does not precede date")
                    

                flight = Flight.objects.create(
                                arrival_airport=icao_arrival,
                                departure_details=icao_departure,
                                aircraft = aircraft,
                                arrival=serializer.validated_data["arrival"],
                                departure=serializer.validated_data["departure"]
                            )

                flight.save()
                    
                data = {
                    "id": flight.id,
                    "arrival_airport": {
                        "name": arrival_airport.name,
                        "ICAO": arrival_airport.icao,
                        "city":arrival_airport.city,
                        "country":arrival_airport.country,
                    },
                    "departure_airport": {
                        "name": departure_airport.name,
                        "ICAO": departure_airport.icao,
                        "city":departure_airport.city,
                        "country":departure_airport.country,
                    },
                    "arrival": flight.arrival,
                    "departure": flight.departure,
                    "aircraft":flight.aircraft
                }
                
                return response.Response(data, status=status.HTTP_201_CREATED)
            
        except Exception as error:
            return response.Response(
                data={"message": f"{error}"}, status=status.HTTP_400_BAD_REQUEST
            )   


class TimeIntervalListFlightView(generics.ListAPIView):
    serializer_class = FlightSerializer
    queryset = Flight
    
    def get(self, request, *args, **kwargs):
        try:
            start = timezone.make_aware(datetime.strptime(kwargs["departure"], "%d-%m-%Y-%H:%M:%S"))
            stop = timezone.make_aware(datetime.strptime(kwargs["arrival"], "%d-%m-%Y-%H:%M:%S"))
            airports = AirPortInfo.objects.all()
            departure_airport_list = Flight.objects.filter(
                departure__gt=start, arrival__lt=stop
            )
            data = []
            for info in departure_airport_list:
                print(start, stop)
                a_airport = airports.get(icao=info.arrival_airport)
                
                d_airport = airports.get(icao=info.depature_airport)
                
                data.append({
                    "dparture_airport":{
                                    "name":d_airport.name,
                                    "ICAO": d_airport.icao,
                                    "city": d_airport.city,
                                    "country": a_airport.country,
                                    "lat": d_airport.lat,
                                    "lon": d_airport.lon,
                                    "time_zone": d_airport.tz,
                                    "flights": d_airport
                                    },
                    "arrival_airport":{
                                    "name":a_airport.name,
                                    "ICAO": a_airport.icao,
                                    "city": a_airport.city,
                                    "country": a_airport.country,
                                    "lat": a_airport.lat,
                                    "lon": a_airport.lon,
                                    "time_zone": a_airport.tz,
                                    "flights": a_airport
                                    },
                    
                    "aircraft": {
                        "serial number":info.aircraft.serial_number,
                        },
                    # "time_interval": abs((( info.arrival - info.departure).total_seconds()) // 60)        
                    
                })
            
            return response.Response(data, status=status.HTTP_200_OK)

        except Exception as error:
            return response.Response(
                {"error": error}, status=status.HTTP_400_BAD_REQUEST
            )



