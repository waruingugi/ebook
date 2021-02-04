from django.test import TestCase
from unittest.mock import patch
from payments.tasks import (
    query_transactions, validate_transaction
)


class QueryTransactionsTaskTest(TestCase):
    def test_query_transactions(self):
        with patch('payments.tasks.africastalking') as payment:
            return_data = [
                {'category': 'MobileC2B', 'clientAccount': '0704845040', 'creationTime': '2021-01-18 17:49:11', 'description': 'Received Mobile C2B Payment from +254704845040', 'destination': 'PaymentWallet', 'destinationType': 'Wallet', 'productName': 'RORO INNOVATIONS', 'provider': 'Mpesa', 'providerChannel': '686105', 'providerMetadata': {'[Personal Details][First Name]': 'WARUI', '[Personal Details][Last Name]': 'NGUGI', '[Personal Details][Middle Name]': 'NGUGI'}, 'providerRefId': 'PAI9R8CLER', 'requestMetadata': {}, 'source': '+254704845040', 'sourceType': 'PhoneNumber', 'status': 'Success', 'transactionDate': '20210118204910', 'transactionFee': 'KES 1.0000', 'transactionId': 'ATPid_89f0f61468787fbb33c8c39f4219bd18', 'value': 'KES 100.0000'}  # noqa
            ]
            payment.product_transactions.return_value = return_data

            response = query_transactions()

        self.assertIsNotNone(response)

    def test_query_transactions_raises_an_error(self):
        with patch('payments.tasks.query_transactions') as mock_query_transactions:
            mock_query_transactions.side_effect = Exception("Internal Server Error")
            self.assertRaises(Exception, query_transactions())


class ValidateTransactionTest(TestCase):
    def test_transaction_is_valid(self):
        with patch('payments.tasks.query_transactions') as mock_query_transactions:
            return_data = [
                {'category': 'MobileC2B', 'clientAccount': '0704845040', 'creationTime': '2021-01-18 17:49:11', 'description': 'Received Mobile C2B Payment from +254704845040', 'destination': 'PaymentWallet', 'destinationType': 'Wallet', 'productName': 'RORO INNOVATIONS', 'provider': 'Mpesa', 'providerChannel': '686105', 'providerMetadata': {'[Personal Details][First Name]': 'WARUI', '[Personal Details][Last Name]': 'NGUGI', '[Personal Details][Middle Name]': 'NGUGI'}, 'providerRefId': 'PAI9R8CLER', 'requestMetadata': {}, 'source': '+254704845040', 'sourceType': 'PhoneNumber', 'status': 'Success', 'transactionDate': '20210118204910', 'transactionFee': 'KES 1.0000', 'transactionId': 'ATPid_89f0f61468787fbb33c8c39f4219bd18', 'value': 'KES 100.0000'}, {'category': 'MobileC2B', 'clientAccount': '0704845040', 'creationTime': '2021-01-18 17:26:59', 'description': 'Received Mobile C2B Payment from +254704845040', 'destination': 'PaymentWallet', 'destinationType': 'Wallet', 'productName': 'RORO INNOVATIONS', 'provider': 'Mpesa', 'providerChannel': '686105', 'providerMetadata': {'[Personal Details][First Name]': 'WARUI', '[Personal Details][Last Name]': 'NGUGI', '[Personal Details][Middle Name]': 'NGUGI'}, 'providerRefId': 'PAI5R7886T', 'requestMetadata': {}, 'source': '+254704845040', 'sourceType': 'PhoneNumber', 'status': 'Success', 'transactionDate': '20210118202657', 'transactionFee': 'KES 1.0000', 'transactionId': 'ATPid_a7afac4f5291cab150cf3c82c327e579', 'value': 'KES 100.0000'}  # noqa
            ]
            mock_query_transactions.return_value = return_data

            payment_status = validate_transaction('PAI5R7886T')
            self.assertTrue(payment_status)

    def test_transaction_is_invalid(self):
        with patch('payments.tasks.query_transactions') as mock_query_transactions:
            return_data = [
                {'category': 'MobileC2B', 'clientAccount': '0704845040', 'creationTime': '2021-01-18 17:49:11', 'description': 'Received Mobile C2B Payment from +254704845040', 'destination': 'PaymentWallet', 'destinationType': 'Wallet', 'productName': 'RORO INNOVATIONS', 'provider': 'Mpesa', 'providerChannel': '686105', 'providerMetadata': {'[Personal Details][First Name]': 'WARUI', '[Personal Details][Last Name]': 'NGUGI', '[Personal Details][Middle Name]': 'NGUGI'}, 'providerRefId': 'PAI9R8CLER', 'requestMetadata': {}, 'source': '+254704845040', 'sourceType': 'PhoneNumber', 'status': 'Success', 'transactionDate': '20210118204910', 'transactionFee': 'KES 1.0000', 'transactionId': 'ATPid_89f0f61468787fbb33c8c39f4219bd18', 'value': 'KES 100.0000'}, {'category': 'MobileC2B', 'clientAccount': '0704845040', 'creationTime': '2021-01-18 17:26:59', 'description': 'Received Mobile C2B Payment from +254704845040', 'destination': 'PaymentWallet', 'destinationType': 'Wallet', 'productName': 'RORO INNOVATIONS', 'provider': 'Mpesa', 'providerChannel': '686105', 'providerMetadata': {'[Personal Details][First Name]': 'WARUI', '[Personal Details][Last Name]': 'NGUGI', '[Personal Details][Middle Name]': 'NGUGI'}, 'providerRefId': 'PAI5R7886T', 'requestMetadata': {}, 'source': '+254704845040', 'sourceType': 'PhoneNumber', 'status': 'Success', 'transactionDate': '20210118202657', 'transactionFee': 'KES 1.0000', 'transactionId': 'ATPid_a7afac4f5291cab150cf3c82c327e579', 'value': 'KES 100.0000'}  # noqa
            ]
            mock_query_transactions.return_value = return_data

            payment_status = validate_transaction('GUESSWORKTRANSACTION')
            self.assertFalse(payment_status)
