from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from fleet_manager_api.models import AirPortInfo


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
        self.airport_id = self.airport.icao

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
        res_fail = self.client.post(reverse(self.list_create_aircrafts_url), self.airport_info)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res_fail.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_airport(self):
        res = self.client.get(reverse(self.airport_url, kwargs={"icao": self.airport_id}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get("icao"), self.airport_id)

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
            reverse(self.airport_url, kwargs={"icao": self.airport_id}),
            airport_info,
        )

        res_fail_put = self.client.put(reverse(self.airport_url, kwargs={"icao": self.airport_id}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get("name"), "Sister-Margret")
        self.assertEqual(res.data.get("city"), "Anchor-Point")
        self.assertEqual(res_fail_put.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_airport(self):
        airport_info_patch = {"name": "Sister Magret"}
        res = self.client.patch(
            reverse(self.airport_url, kwargs={"icao": self.airport_id}),
            airport_info_patch,
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get("name"), "Sister Magret")

    def test_delete_airport(self):
        res = self.client.delete(reverse(self.airport_url, kwargs={"icao": self.airport_id}))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
