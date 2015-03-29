__author__ = 'diego'
import unittest
from django.test import Client


class GetMethods(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_get_hives(self):
        # Issue a GET request.
        response = self.client.get('/hives/')

        print("testing_get_hives")

        print("Response: ")
        print(response.body)
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)