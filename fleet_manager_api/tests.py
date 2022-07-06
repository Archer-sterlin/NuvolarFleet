import uuid
from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Aircraft, AirPortInfo, Flight


class TestAircraftEndpoint(APITestCase):
    def setUp(self):
        self.list_create_aircrafts_url = "list-create-aircrafts"
        self.aircraft_url = "aircraft"

        self.aircraft_info = {
            "serial_number": "yuoar-rlaovun-niaps-anolecrab",
            "manufacturer": "Scorpion",
        }
        self.aircraft_info2 = {
            "serial_number": "yuoalr-rlaovun-niaps-anolecrab",
            "manufacturer": "Scorpion",
        }

        self.aircraft_info_put = {
            "serial_number": "yuoalr-rlaovun-niaps-anolecrab",
            "manufacturer": "Scorpion",
        }

        self.aircraft_info_patch = {
            "serial_number": "yuoalr-rlaovun-niaps-anolecrab",
        }

        self.aircraft = Aircraft.objects.create(**self.aircraft_info2)
        self.aircraft_id = str(self.aircraft.id)
        self.aircraft.save()

    def test_list_aircraft(self):
        res = self.client.get(reverse(self.list_create_aircrafts_url))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(res.data), 1)

    def test_create_aircraft(self):
        res_create = self.client.post(
            reverse(self.list_create_aircrafts_url), self.aircraft_info
        )
        res_fail = self.client.post(
            reverse(self.list_create_aircrafts_url), self.aircraft_info
        )
        self.assertEqual(res_create.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res_fail.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_aircraft(self):
        res = self.client.get(
            reverse(self.aircraft_url, kwargs={"pk": self.aircraft_id})
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get("id"), self.aircraft_id)

    def test_put_aircraft(self):
        res = self.client.put(
            reverse(self.aircraft_url, kwargs={"pk": self.aircraft_id}),
            self.aircraft_info_put,
        )

        res_fail_put = self.client.put(
            reverse(self.aircraft_url, kwargs={"pk": self.aircraft_id})
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res_fail_put.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_aircraft(self):
        aircraft_info_patch = {"manufacturer": "Tesla"}

        res = self.client.patch(
            reverse(self.aircraft_url, kwargs={"pk": self.aircraft_id}),
            aircraft_info_patch,
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_aircraft(self):
        res = self.client.delete(
            reverse(self.aircraft_url, kwargs={"pk": self.aircraft_id})
        )

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)


class TestAirPortInfoEndpoint(APITestCase):
    def setUp(self):
        self.list_create_aircrafts_url = "list-create-airports"
        self.airport_url = "airport"
        self.airport_info = {
            "icao": "06ML",
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
        self.airport.save()

    def test_list_airport(self):
        res = self.client.get(reverse(self.list_create_aircrafts_url))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(res.data), 1)

    def test_create_airport(self):
        airport_info = {
            "icao": "16ML",
            "name": "Sister Margret",
            "city": "Anchor Point",
            "subd": "Alaska",
            "country": "US",
            "elevation": 450,
            "lat": 59.94919968,
            "lon": -151.695999146,
            "tz": "America/Anchorage",
        }
        res = self.client.post(reverse(self.list_create_aircrafts_url), airport_info)
        res_fail = self.client.post(
            reverse(self.list_create_aircrafts_url), self.airport_info
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res_fail.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_airport(self):
        res = self.client.get(reverse(self.airport_url, kwargs={"pk": self.airport_id}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(uuid.UUID(res.data.get("id")), self.airport_id)

    def test_put_airport(self):
        airport_info = {
            "icao": "16ML",
            "name": "Sister-Margret",
            "city": "Anchor-Point",
            "subd": "Alaska",
            "country": "US",
            "elevation": 450,
            "lat": 59.94919968,
            "lon": -151.695999146,
            "tz": "America/Anchorage",
        }
        res = self.client.put(
            reverse(self.airport_url, kwargs={"pk": self.airport_id}),
            airport_info,
        )

        res_fail_put = self.client.put(
            reverse(self.airport_url, kwargs={"pk": self.airport_id})
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get("name"), "Sister-Margret")
        self.assertEqual(res.data.get("city"), "Anchor-Point")
        self.assertEqual(res_fail_put.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_airport(self):
        airport_info_patch = {"name": "Sister Magret"}
        res = self.client.patch(
            reverse(self.airport_url, kwargs={"pk": self.airport_id}),
            airport_info_patch,
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get("name"), "Sister Magret")

    def test_delete_airport(self):
        res = self.client.delete(
            reverse(self.airport_url, kwargs={"pk": self.airport_id})
        )

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)


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

        self.tomorrow = timezone.now() + timedelta(days=1)
        self.next_tomorrow = timezone.now() + timedelta(days=2)
        self.three_days_from_now = timezone.now() + timedelta(days=2)

        self.aircraft = Aircraft.objects.create(**self.aircraft_info)
        self.aircraft.save()
        self.aircraft_id = self.aircraft.id

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
        self.airport.save()

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
        self.airport2.save()

        self.flight_info = {
            "departure_airport": "88GG",
            "arrival_airport": "96GG",
            "departure": self.tomorrow,
            "arrival": self.next_tomorrow,
            "aircraft": self.aircraft,
            "updated_at": "2022-07-06T12:23:55.838418Z",
            "created_at": "2022-07-06T12:23:55.833731Z",
        }

        self.flight_info2 = {
            "departure_airport": "96GG",
            "arrival_airport": "88GG",
            "departure": self.tomorrow,
            "arrival": self.next_tomorrow,
            "aircraft": self.aircraft_id,
            "updated_at": "2022-07-06T12:23:55.838418Z",
            "created_at": "2022-07-06T12:23:55.833731Z",
        }
        self.flight = Flight.objects.create(**self.flight_info)
        self.flight.save()
        self.flight_id = self.flight.id

    def test_list_flights(self):
        res = self.client.get(reverse(self.flight_url))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(res.data), 1)

    def test_create_flight(self):
        res = self.client.post(reverse(self.flight_url), self.flight_info2)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_get_flight(self):
        res = self.client.get(
            reverse(self.edit_flight_url, kwargs={"pk": self.flight_id})
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(uuid.UUID(res.data.get("id")), self.flight_id)

    def test_delete_flight(self):
        res = self.client.delete(
            reverse(self.edit_flight_url, kwargs={"pk": self.flight_id})
        )
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_put_flight(self):
        flight_info = {
            "departure_airport": "96GG",
            "arrival_airport": "88GG",
            "departure": self.tomorrow,
            "arrival": self.three_days_from_now,
            "aircraft": self.aircraft_id,
        }
        res = self.client.put(
            reverse(self.edit_flight_url, kwargs={"pk": self.flight_id}), flight_info
        )
        res_arrival = res.data.get("arrival").replace("T", " ")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res_arrival[0:-1], str(self.three_days_from_now)[0:-6])

    def test_patch_flight(self):
        flight_info = {
            "departure_airport": "96GG",
            "arrival_airport": "88GG",
            "departure": self.tomorrow,
            "arrival": self.next_tomorrow,
            "aircraft": self.aircraft_id,
        }
        res = self.client.patch(
            reverse(self.edit_flight_url, kwargs={"pk": self.flight_id}), flight_info
        )

        res_arrival = res.data.get("arrival").replace("T", " ")
        res_departure = res.data.get("departure").replace("T", " ")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res_arrival[0:-1], str(self.next_tomorrow)[0:-6])
        self.assertEqual(res_departure[0:-1], str(self.tomorrow)[0:-6])

    def test_search_by_departure(self):
        res_empty = self.client.get(
            reverse(self.search_departure_url, kwargs={"icao": "883GG"})
        )
        res = self.client.get(
            reverse(self.search_departure_url, kwargs={"icao": "88GG"})
        )
        self.assertEqual(res_empty.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_empty.data), 0)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(res.data), 1)

    def test_search_by_arrival(self):
        res_empty = self.client.get(
            reverse(self.search_arrival_url, kwargs={"icao": "883GG"})
        )
        res = self.client.get(reverse(self.search_arrival_url, kwargs={"icao": "96GG"}))
        self.assertEqual(res_empty.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_empty.data), 0)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(res.data), 1)

    def test_search_by_departure_time_interval(self):
        res = self.client.get(
            reverse(
                self.list_departure_time_url,
                kwargs={"from": "06-07-2022-08:00:00", "to": "06-08-2022-08:00:00"},
            )
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(res.data), 1)
