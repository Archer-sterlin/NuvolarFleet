from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Aircraft, AirPortInfo, Flight


class TestListCreatAircraft(APITestCase):
    def setUp(self):
        self.list_create_aircrafts_url = "list-create-aircrafts"
        self.aircraft_info = {
            "serial_number": "yuoalr-rlaovun-niaps-anolecrab",
            "manufacturer": "Scorpion",
        }

    def test_create_list_airport(self):
        res_get = self.client.get(reverse(self.list_create_aircrafts_url))
        res_create = self.client.post(reverse(self.list_create_aircrafts_url), self.aircraft_info)
        res_fail = self.client.post(
            reverse(self.list_create_aircrafts_url),
            json={"serial_number": "yuoalr-rlaovun-niaps-anolecrab", "manufacturer": "Scorpion"},
        )

        self.assertEqual(res_get.status_code, status.HTTP_200_OK)
        self.assertEqual(res_create.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res_fail.status_code, status.HTTP_400_BAD_REQUEST)


class TestListUpdateRetiveDeleteAircraft(APITestCase):
    aircraft_id = ""

    def setUp(self):
        self.aircraft_url = "aircraft"
        aircraft_info = {
            "serial_number": "yuoalr-rlaovun-niaps-anolecrab",
        }

        self.aircraft = Aircraft.objects.create(**aircraft_info)
        self.aircraft_id = str(self.aircraft.id)

        self.aircraft.save()

    def test_get_airport(self):
        aircraft_info_put = {
            "serial_number": "yuoalr-rlaovun-niaps-anolecrab",
            "manufacturer": "Scorpion",
        }

        aircraft_info_patch = {"manufacturer": "Tesla"}

        res_get = self.client.get(reverse(self.aircraft_url, kwargs={"pk": self.aircraft.id}))
        res_put = self.client.put(
            reverse(self.aircraft_url, kwargs={"pk": self.aircraft.id}), aircraft_info_put
        )
        res_fail_put = self.client.put(
            reverse(self.aircraft_url, kwargs={"pk": self.aircraft.id}), aircraft_info_patch
        )
        res_patch = self.client.patch(
            reverse(self.aircraft_url, kwargs={"pk": self.aircraft.id}), aircraft_info_patch
        )
        res_delete = self.client.delete(reverse(self.aircraft_url, kwargs={"pk": self.aircraft.id}))

        self.assertEqual(res_get.status_code, status.HTTP_200_OK)
        self.assertEqual(res_put.status_code, status.HTTP_200_OK)
        self.assertEqual(res_fail_put.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res_patch.status_code, status.HTTP_200_OK)
        self.assertEqual(res_delete.status_code, status.HTTP_204_NO_CONTENT)
