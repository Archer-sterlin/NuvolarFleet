from datetime import datetime

import airportsdata
from django.utils import timezone
from rest_framework import generics, response, status

from .models import Aircraft, AirPortInfo, Flight
from .serializers import (AircraftSerializer, AirPortInfoSerializer,
                          FlightSerializer)

airports = airportsdata.load()

now = timezone.now()


class AirCraftView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AircraftSerializer
    queryset = Aircraft.objects.all()


class ListAirCraftView(generics.ListCreateAPIView):
    serializer_class = AircraftSerializer
    queryset = Aircraft.objects.all()


class AirportInfoView(generics.ListCreateAPIView):
    serializer_class = AirPortInfoSerializer
    queryset = AirPortInfo.objects.all()


class EditAirportInfoView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AirPortInfoSerializer
    queryset = AirPortInfo.objects.all()


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

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                airport = AirPortInfo.objects.all()
                icao_arrival = (
                    serializer.validated_data["arrival_airport"][0:2]
                    + serializer.validated_data["arrival_airport"][2:].upper()
                )
                icao_departure = (
                    serializer.validated_data["departure_airport"][0:2]
                    + serializer.validated_data["departure_airport"][2:].upper()
                )
                arrival_airport = airport.get(icao=icao_arrival)
                arrival = serializer.validated_data["arrival"]
                departure = serializer.validated_data["departure"]
                departure_airport = airport.get(icao=icao_departure)
                aircraft = serializer.validated_data["aircraft"]

                if icao_arrival == icao_departure:
                    raise Exception("arrival airport cannot be the same as departure airport")

                if (arrival <= departure) or (departure < now):
                    raise Exception(
                        "Invalid date, make sure dates are future date and arrival date does not precede date"
                    )

                flight = Flight.objects.create(
                    arrival_airport=icao_arrival,
                    departure_airport=icao_departure,
                    aircraft=aircraft,
                    arrival=serializer.validated_data["arrival"],
                    departure=serializer.validated_data["departure"],
                )

                flight.save()

                data = {
                    "id": flight.id,
                    "departure_airport": {
                        "name": departure_airport.name,
                        "ICAO": departure_airport.icao,
                        "city": departure_airport.city,
                        "country": departure_airport.country,
                    },
                    "arrival_airport": {
                        "name": arrival_airport.name,
                        "ICAO": arrival_airport.icao,
                        "city": arrival_airport.city,
                        "country": arrival_airport.country,
                    },
                    "arrival": flight.arrival,
                    "departure": flight.departure,
                    "aircraft": {
                        "serial number": flight.aircraft.serial_number,
                        "manufacturer": flight.aircraft.manufacturer,
                    },
                }

                return response.Response(data, status=status.HTTP_201_CREATED)

        except Exception as error:
            return response.Response(
                data={"message": f"{error}"}, status=status.HTTP_400_BAD_REQUEST
            )


class EditFlightScheduleView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FlightSerializer
    queryset = Flight.objects.all()


class TimeIntervalListFlightView(generics.ListAPIView):
    serializer_class = FlightSerializer
    queryset = Flight

    def get(self, request, *args, **kwargs):
        try:
            start = timezone.make_aware(datetime.strptime(kwargs["from"], "%d-%m-%Y-%H:%M:%S"))
            stop = timezone.make_aware(datetime.strptime(kwargs["to"], "%d-%m-%Y-%H:%M:%S"))
            if start > stop:
                raise ValueError("start time range cannot be ahead of stop time range")

            airports = AirPortInfo.objects.all()
            departure_airport_list = Flight.objects.filter(departure__gt=start, departure__lt=stop)
            data = []
            for info in departure_airport_list:
                d_airport = airports.get(icao=info.departure_airport)
                data.append(
                    {
                        "departure_airport": {
                            "name": d_airport.name,
                            "ICAO": d_airport.icao,
                            "city": d_airport.city,
                            "country": d_airport.country,
                            "lat": d_airport.lat,
                            "lon": d_airport.lon,
                            "time_zone": d_airport.tz,
                            "flights": departure_airport_list.filter(
                                departure_airport=d_airport.icao
                            ).count(),
                        },
                        "aircraft": {
                            "serial_number": info.aircraft.serial_number,
                            "flight time": abs(
                                ((info.arrival - info.departure).total_seconds()) // 60
                            ),
                        },
                    }
                )

            return response.Response(data, status=status.HTTP_200_OK)

        except Exception as error:
            return response.Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)
