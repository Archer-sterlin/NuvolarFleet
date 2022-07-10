from django.urls import path

from .views import (
    AirCraftView,
    AirportInfoView,
    ArrivalFlightsView,
    DepartureFlightsView,
    EditAirportInfoView,
    EditFlightScheduleView,
    FlightScheduleView,
    ListAirCraftView,
    TimeIntervalListFlightView,
)

urlpatterns = [
    # aircraft CRUD operations
    path("aircrafts/", ListAirCraftView.as_view(), name="list-create-aircrafts"),
    path("aircrafts/<uuid:pk>/", AirCraftView.as_view(), name="aircraft"),
    # airport CRUD operations
    path("airport/", AirportInfoView.as_view(), name="list-create-airports"),
    path("airport/<icao>/", EditAirportInfoView.as_view(), name="airport"),
    # flight CRUD operations
    path("flight/", FlightScheduleView.as_view(), name="list-create-flight"),
    path("flight/edit/<uuid:pk>/", EditFlightScheduleView.as_view(), name="edit-flight"),
    path(
        "flights/departure/time/range/<from>/<to>/",
        TimeIntervalListFlightView.as_view(),
        name="list-departure-time",
    ),
    path(
        "flights/departure/<icao>/",
        DepartureFlightsView.as_view(),
        name="search-departure",
    ),
    path("flights/arrival/<icao>/", ArrivalFlightsView.as_view(), name="search-arrival"),
]
