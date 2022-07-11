from datetime import timedelta

from django.utils import timezone
from rest_framework.test import APITestCase

from fleet_manager_api.models import Aircraft, AirPortInfo, Flight


class TestModel(APITestCase):
    def setUp(self):
        self.tomorrow = timezone.now() + timedelta(days=1)
        self.next_tomorrow = timezone.now() + timedelta(days=2)
        self.three_days_from_now = timezone.now() + timedelta(days=2)

        self.aircraft = Aircraft.objects.create(
            serial_number="rlaovun-yuoar-niaps-anolecrab", manufacturer="Scorpion"
        )

        self.airport = AirPortInfo.objects.create(
            icao="96GG",
            name="Luxaviation",
            city="Anchor Point",
            subd="Alaska",
            country="US",
            elevation=450.00,
            lat=59.94919968,
            lon=-151.695999146,
            tz="America/Anchorage",
        )

    def test_aircraft(self):
        aircraft = Aircraft.objects.create(
            serial_number="yuoar-rlaovun-niaps-anolecrab", manufacturer="Scorpion"
        )

        self.assertIsInstance(aircraft, Aircraft)
        self.assertEqual(aircraft.serial_number, "yuoar-rlaovun-niaps-anolecrab")
        self.assertEqual(aircraft.manufacturer, "Scorpion")
        self.assertEqual(str(aircraft), "yuoar-rlaovun-niaps-anolecrab - Scorpion")

    def test_airport_model(self):
        airport = AirPortInfo.objects.create(
            icao="06ML",
            name="Luxaviation",
            city="Anchor Point",
            subd="Alaska",
            country="US",
            elevation=450.00,
            lat=59.94919968,
            lon=-151.695999146,
            tz="America/Anchorage",
        )

        self.assertIsInstance(airport, AirPortInfo)
        self.assertEqual(airport.icao, "06ML")
        self.assertNotEqual(airport.icao, " ")
        self.assertEqual(len(airport.icao), 4)
        self.assertIsInstance(airport.elevation, float)
        self.assertIsInstance(airport.lat, float)
        self.assertIsInstance(airport.lon, float)
        self.assertEqual(str(airport), "06ML - Luxaviation")

    def test_flight_model(self):

        flight_info2 = {
            "departure_airport": "96GG",
            "arrival_airport": "88GG",
            "departure": self.tomorrow,
            "arrival": self.next_tomorrow,
            "aircraft": self.aircraft,
            "updated_at": "2022-07-06T12:23:55.838418Z",
            "created_at": "2022-07-06T12:23:55.833731Z",
        }
        flight = Flight.objects.create(**flight_info2)
        self.assertEqual(flight.departure_airport, "96GG")
        self.assertEqual(flight.departure_airport, self.airport.icao)
        self.assertEqual(flight.arrival_airport, "88GG")
        self.assertGreaterEqual(flight.departure, timezone.now())
        self.assertGreater(flight.arrival, flight.departure)
        self.assertNotEqual(flight.arrival_airport, flight.departure_airport)
        self.assertIsInstance(flight, Flight)
