from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import generics, response, status
from .serializers import AirPortInfoSerializer, FlightScheduleSerializer, FlightSerializer, AircraftSerializer
from .models import AirPortInfo, ArrivalInfo, DepartureInfo, Flight, Aircraft
import airportsdata


airports_data = airportsdata.load()
CIAOs = airports_data.keys()

# Create your views here.
class AirCraftView(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]
    serializer_class = AircraftSerializer
    queryset = Aircraft.objects.all()


class AirportInfoView(generics.ListCreateAPIView):
    serializer_class = AirPortInfoSerializer
    queryset = AirPortInfo.objects.all()
    
    
class FlightScheduleView(generics.CreateAPIView):
    serializer_class = FlightScheduleSerializer
    queryset = Flight.objects.all()
    
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                arrival_at = serializer.validated_data["arrival_airport_icao"]
                departure_at = serializer.validated_data["departure_airport_icao"]
                arrival_time = serializer.validated_data["arrival_time"]
                departure_time = serializer.validated_data["departure_time"]
               
                airports = AirPortInfo.objects.all()
                arrival_airport = airports.get(icao=arrival_at)
                departure_airport = airports.get(icao=departure_at)
             
                arrival_airport.save()    
                departure_airport.save()
                          
                arrival_info = ArrivalInfo.objects.create(
                    airport_info=arrival_airport,
                    estemated_time=arrival_time  
                )
                arrival_info.save()
                
                departure_info = DepartureInfo.objects.create(
                    airport_info=departure_airport,
                    estemated_time=departure_time  
                )
                departure_info.save()
                
                flight = Flight.objects.create(
                    arrival_details=arrival_info,
                    departure_details=departure_info,
                )
            
                flight.save()
                data = {
                    "id":flight.id,
                    "arrival_airport":{
                        "name":flight.arrival_details.airport_info.name,
                        "ICAO":flight.arrival_details.airport_info.icao,
                        },
                    "departure_airport":{
                        "name":flight.departure_details.airport_info.name,
                        "ICAO":flight.departure_details.airport_info.icao,
                        },
                    "arrival_time":arrival_time,
                    "departure_time":departure_time
                }
                return response.Response(data, status=status.HTTP_201_CREATED)
          
        except Exception as error:
             return response.Response(data={"message":f"{error}"}, status=status.HTTP_400_BAD_REQUEST)
            

class ListFlightView(generics.ListAPIView):
    serializer_class = FlightSerializer
    queryset = Flight.objects.all()
    
    def get(self, request, *args, **kwargs):
        try:
            flight_list = Flight.objects.all()
            return flights(flight_list)

        except Exception as error:
            return response.Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)


    
def flights(flight_list):
    data = []
    print(flight_list)
    for flight in flight_list:
        data.append( { 
                "id":flight.id,
                "arrival_airport":{
                    "name":flight.arrival_details.airport_info.name,
                    "ICAO":flight.arrival_details.airport_info.icao,
                    },
                "departure_airport":{
                    "name":flight.departure_details.airport_info.name,
                    "ICAO":flight.departure_details.airport_info.icao,
                    },
                "arrival_time":flight.arrival_details.estemated_time,
                "departure_time":flight.departure_details.estemated_time,   
        })
  
    return response.Response(data, status=status.HTTP_200_OK)