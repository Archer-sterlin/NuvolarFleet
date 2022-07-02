from django.urls import path
from .views import (
    AirCraftView,
    AirportInfoView,
    FlightScheduleView,
    ListFlightView,
)


app_name = "nuvolar-fleet-api"

urlpatterns = [
    path("aircrafts/", AirCraftView.as_view(), name="aircraft"),
    path("airport/", AirportInfoView.as_view(), name="airport"),
    path("schedule/flight/", FlightScheduleView.as_view(), name="flight-schedule"),
    path("flights/", ListFlightView.as_view(), name="flight-list"),
]
