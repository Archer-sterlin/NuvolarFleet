from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


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
