import uuid
from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from fleet_manager_api.models import Aircraft, AirPortInfo, Flight


class TestFlightEndpoint(APITestCase):
    def setUp(self):
        self.flight_url = "list-create-flight"
        self.edit_flight_url = "edit-flight"
        self.list_departure_time_url = "list-departure-time"
        self.search_departure_url = "search-departure"
        self.search_arrival_url = "search-arrival"

        self.aircraft_info = {
            "serial_number": "yuoalr-rlaovun-niaps-anolecrab",
            "manufacturer": "Scorpion",
        }
        self.aircraft_info2 = {
            "serial_number": "oalr-rlaovun-nie64aps-anolecrab",
            "manufacturer": "Tesla",
        }
        self.aircraft_info3 = {
            "serial_number": "yuoa-aovun-iap-anolecrab",
            "manufacturer": "Scorpion",
        }

        self.tomorrow = timezone.now() + timedelta(days=1)
        self.next_tomorrow = timezone.now() + timedelta(days=2)
        self.three_days_from_now = timezone.now() + timedelta(days=2)

        self.aircraft = Aircraft.objects.create(**self.aircraft_info)
        self.aircraft2 = Aircraft.objects.create(**self.aircraft_info2)
        self.aircraft3 = Aircraft.objects.create(**self.aircraft_info3)

        self.airport_info = {
            "icao": "96GG",
            "name": "Luxaviation",
            "city": "Anchor Point",
            "subd": "Alaska",
            "country": "US",
            "elevation": 450,
            "lat": 59.94919968,
            "lon": -151.695999146,
            "tz": "America/Anchorage",
        }
        self.airport = AirPortInfo.objects.create(**self.airport_info)
        self.airport_id = self.airport.id

        self.airport_info2 = {
            "icao": "88GG",
            "name": "Nuvolar",
            "city": "Anchor Point",
            "subd": "Alaska",
            "country": "US",
            "elevation": 450,
            "lat": 55.94919968,
            "lon": -191.695999146,
            "tz": "America/Anchorage",
        }
        self.airport2 = AirPortInfo.objects.create(**self.airport_info2)
        self.airport2_id = self.airport2.id

        self.flight_info = {
            "departure_airport": "88GG",
            "arrival_airport": "96GG",
            "departure": self.tomorrow,
            "arrival": self.next_tomorrow,
            "aircraft": self.aircraft.id,
            "updated_at": "2022-07-06T12:23:55.838418Z",
            "created_at": "2022-07-06T12:23:55.833731Z",
        }

        self.flight_info2 = {
            "departure_airport": "96GG",
            "arrival_airport": "88GG",
            "departure": self.tomorrow,
            "arrival": self.next_tomorrow,
            "aircraft": self.aircraft2,
            "updated_at": "2022-07-06T12:23:55.838418Z",
            "created_at": "2022-07-06T12:23:55.833731Z",
        }

        self.flight_info3 = {
            "departure_airport": "96GG",
            "arrival_airport": "88GG",
            "departure": self.tomorrow + timedelta(days=1),
            "arrival": self.next_tomorrow + timedelta(days=1),
            "aircraft": self.aircraft3,
            "updated_at": "2022-07-06T12:23:55.838418Z",
            "created_at": "2022-07-06T12:23:55.833731Z",
        }
        self.flight = Flight.objects.create(**self.flight_info2)
        self.flight3 = Flight.objects.create(**self.flight_info3)

    def test_list_flights(self):
        res = self.client.get(reverse(self.flight_url))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(res.data), 0)

    def test_create_flight(self):
        res = self.client.post(reverse(self.flight_url), self.flight_info)
        res2 = self.client.post(reverse(self.flight_url), self.flight_info2)
        res3 = self.client.post(reverse(self.flight_url), self.flight_info3)
        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res3.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_get_flight(self):
        res = self.client.get(reverse(self.edit_flight_url, kwargs={"pk": self.flight.id}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(uuid.UUID(res.data.get("id")), self.flight.id)

    def test_delete_flight(self):
        res = self.client.delete(reverse(self.edit_flight_url, kwargs={"pk": self.flight.id}))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_put_flight(self):
        flight_info = {
            "departure_airport": "96GG",
            "arrival_airport": "88GG",
            "departure": self.tomorrow,
            "arrival": self.three_days_from_now,
            "aircraft": self.aircraft.id,
        }
        res = self.client.put(
            reverse(self.edit_flight_url, kwargs={"pk": self.flight.id}), flight_info
        )
        res_arrival = res.data.get("arrival")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res_arrival, self.three_days_from_now)

    def test_patch_flight(self):
        flight_info = {
            "departure_airport": "96GG",
            "arrival_airport": "88GG",
            "departure": self.tomorrow,
            "arrival": self.next_tomorrow,
            "aircraft": self.aircraft.id,
        }
        res = self.client.patch(
            reverse(self.edit_flight_url, kwargs={"pk": self.flight.id}), flight_info
        )
        res_arrival = res.data.get("arrival")
        res_departure = res.data.get("departure")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res_arrival, self.next_tomorrow)
        self.assertEqual(res_departure, self.tomorrow)

    def test_search_by_departure(self):
        res_empty = self.client.get(reverse(self.search_departure_url, kwargs={"icao": "883GG"}))
        res = self.client.get(reverse(self.search_departure_url, kwargs={"icao": "88GG"}))
        self.assertEqual(res_empty.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_empty.data), 0)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(res.data), 0)

    def test_search_by_arrival(self):
        res_empty = self.client.get(reverse(self.search_arrival_url, kwargs={"icao": "883GG"}))
        res = self.client.get(reverse(self.search_arrival_url, kwargs={"icao": "96GG"}))
        self.assertEqual(res_empty.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_empty.data), 0)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(res.data), 0)

    def test_search_by_departure_time_interval(self):
        res = self.client.get(
            reverse(
                self.list_departure_time_url,
                kwargs={"from": "06-07-2022+08:00:00", "to": "06-08-2022+08:00:00"},
            )
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(res.data), 0)
