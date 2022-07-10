from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from fleet_manager_api.models import Aircraft


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
        res_create = self.client.post(reverse(self.list_create_aircrafts_url), self.aircraft_info)
        res_fail = self.client.post(reverse(self.list_create_aircrafts_url), self.aircraft_info)
        self.assertEqual(res_create.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res_fail.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_aircraft(self):
        res = self.client.get(reverse(self.aircraft_url, kwargs={"pk": self.aircraft_id}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get("id"), self.aircraft_id)

    def test_put_aircraft(self):
        res = self.client.put(
            reverse(self.aircraft_url, kwargs={"pk": self.aircraft_id}),
            self.aircraft_info_put,
        )

        res_fail_put = self.client.put(reverse(self.aircraft_url, kwargs={"pk": self.aircraft_id}))
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
        res = self.client.delete(reverse(self.aircraft_url, kwargs={"pk": self.aircraft_id}))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
