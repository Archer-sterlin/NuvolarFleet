from django.urls import path

from .views import (AirCraftView, AirportInfoView, ArrivalFlightsView,
                    DepartureFlightsView, EditAirportInfoView,
                    EditFlightScheduleView, FlightScheduleView,
                    ListAirCraftView, TimeIntervalListFlightView)

app_name = "nuvolar-fleet-api"

urlpatterns = [
    path("aircrafts/", ListAirCraftView.as_view(), name="aircraft-list"),
    path("aircrafts/<uuid:pk>/", AirCraftView.as_view(), name="aircraft"),
    path("airport/", AirportInfoView.as_view(), name="airport-list"),
    path("airport/<uuid:pk>/", EditAirportInfoView.as_view(), name="airport"),
    path("flight/", FlightScheduleView.as_view(), name="flight-list-create"),
    path(
        "flight/edit/<uuid:pk>/", EditFlightScheduleView.as_view(), name="flight-edit"
    ),
    path(
        "flights/depature/time/range/<departure>/<arrival>/",
        TimeIntervalListFlightView.as_view(),
        name="sarch-range",
    ),
    path(
        "flights/depature/<icao>",
        DepartureFlightsView.as_view(),
        name="sarch-departure",
    ),
    path("flights/arrival/<icao>", ArrivalFlightsView.as_view(), name="sarch-arrival"),
]
