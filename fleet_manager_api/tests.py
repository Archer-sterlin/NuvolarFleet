from django.test import TestCase
from django.urls import reverse

# Create your tests here.

class EndpointsTestCase(TestCase):
    def test_list_flights(self):
        self.assertEqual(1+1, 2)
