from django.test import TestCase
from payments.models import Customers
from django.urls import reverse
from unittest.mock import patch
import requests


class IndexViewTest(TestCase):
    @classmethod
    @patch.object(requests, 'post', return_value=200)
    def setUpTestData(cls, mock_requests):
        # Set up non-modified objects used by all test methods
        Customers.objects.create(
            name="Jon Snow",
            email="johnsnow@gmail.com",
            transaction_code='PFA67BN8UO'
        )

    def test_index_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'index.html')

    def test_index_view_url_redirects_to_details_view(self):
        with patch('payments.views.validate_transaction') as mock_validate_transaction:
            mock_validate_transaction.return_value = True
            response = self.client.post(
                '/', {'transaction_code': 'AFA63ZN8UO'}
            )
            self.assertRedirects(response, '/details')

    def test_index_view_returns_error_on_invalid_transaction_code(self):
        with patch('payments.views.validate_transaction') as mock_validate_transaction:
            mock_validate_transaction.return_value = False
            response = self.client.post(
                '/', {'transaction_code': 'AFA63ZN8UO'}
            )
            self.assertEqual(response.status_code, 200)


class DetailsViewTest(TestCase):
    @classmethod
    @patch.object(requests, 'post', return_value=200)
    def setUpTestData(cls, mock_requests):
        # Set up non-modified objects used by all test methods
        Customers.objects.create(
            name="Jon Snow",
            email="jonsnow@gmail.com",
            transaction_code='PFA67BN8UO'
        )

    def test_details_view_url_exists_at_desired_location(self):
        session = self.client.session
        session['transaction_code'] = 'MBA67N8U8'
        session.save()

        response = self.client.get(reverse('details'))
        self.assertTemplateUsed(response, 'details.html')

    @patch.object(requests, 'post', return_value=200)
    def test_details_view_url_redirects_to_success_view(self, mock_requests):
        session = self.client.session
        session['transaction_code'] = 'MBA67N8U8'
        session.save()

        response = self.client.post(
            '/details',
            {'name': 'John', 'email': 'john@gmail.com'}
        )
        self.assertRedirects(response, '/success')

    def test_details_view_returns_error_on_invalid_transaction_code(self):
        session = self.client.session
        session['transaction_code'] = 'MBA67N8U8'
        session.save()

        response = self.client.post(
            '/details',
            {'name': 'Robin', 'email': 'jonsnow@gmail.com'}
        )
        self.assertEqual(response.status_code, 200)


class SuccessViewTest(TestCase):
    def test_success_view_url_exists_at_desired_location(self):
        session = self.client.session
        session['email'] = 'jonsnow@gmail.com'
        session.save()

        response = self.client.get(reverse('success'))
        self.assertTemplateUsed(response, 'success.html')

    def test_details_view_url_redirects_to_success_view(self):
        response = self.client.get(reverse('success'))
        self.assertEqual(response.url, '/details')
