from django.test import TestCase
from payments.forms import (
    TransactionCodeForm, DetailsForm
)
from payments.models import Customers
import requests
from unittest.mock import patch


class TransactionCodeFormTest(TestCase):
    @classmethod
    @patch.object(requests, 'post', return_value=200)
    def setUpTestData(cls, mock_requests):
        # Set up non-modified objects used by all test methods
        Customers.objects.create(
            name="John Doe",
            email="johndoe@gmail.com",
            transaction_code='PAI9R8CLER'
        )

    def test_transactioncode_form_is_valid(self):
        form_data = {
            'transaction_code': 'AAI9R8CLER'
        }
        form = TransactionCodeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_transactioncode_form_is_vinalid(self):
        form_data = {
            'transaction_code': 'PAI9R8CLER'
        }
        form = TransactionCodeForm(data=form_data)
        self.assertTrue(form.has_error('transaction_code'))


class DetailsFormTest(TestCase):
    @classmethod
    @patch.object(requests, 'post', return_value=200)
    def setUpTestData(cls, mock_requests):
        # Set up non-modified objects used by all test methods
        Customers.objects.create(
            name="John Doe",
            email="johndoe@gmail.com",
            transaction_code='PAI9R8CLER'
        )

    def test_details_form_is_valid(self):
        form_data = {
            'name': 'Jon Snow',
            'email': 'jonsnow@gmail.com'
        }
        form = DetailsForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_transactioncode_form_is_vinalid(self):
        form_data = {
            'name': 'Michael',
            'email': 'johndoe@gmail.com'
        }
        form = DetailsForm(data=form_data)
        self.assertTrue(form.has_error('email'))
