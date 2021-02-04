from payments.models import Customers
from django.test import TestCase
from unittest.mock import patch


class SendMessageSignalTest(TestCase):
    def test_signal_sends_message(self):
        with patch('requests.post') as mock_post:
            mock_post.return_value = 200
            Customers.objects.create(
                name="John Doe",
                email="johndoe@gmail.com",
                transaction_code='PAI9R8CLER'
            )

            mock_post.assert_called_once()
