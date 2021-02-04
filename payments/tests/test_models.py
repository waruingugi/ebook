from django.test import TestCase
from payments.models import Customers
import requests
from unittest.mock import patch


class CustomersModelTest(TestCase):
    @classmethod
    @patch.object(requests, 'post', return_value=200)
    def setUpTestData(cls, mock_requests):
        # Set up non-modified objects used by all test methods
        Customers.objects.create(
            name="John Doe",
            email="johndoe@gmail.com",
            transaction_code='PAI9R8CLER'
        )

        Customers.objects.create(
            name="Moses",
            email="mosesdoe@gmail.com",
            transaction_code='PAI9R8CLER1'
        )

    def test_string_representation(self):
        customer = Customers.objects.get(email="johndoe@gmail.com")
        self.assertEqual(str(customer), "John Doe")

    def test_transaction_code_exists(self):
        customer = Customers.objects.get(email="mosesdoe@gmail.com")
        self.assertEquals('PAI9R8CLER1', customer.transaction_code)

    def test_first_name_decorator(self):
        customer = Customers.objects.get(email="johndoe@gmail.com")
        self.assertEquals(customer.first_name, "John")
