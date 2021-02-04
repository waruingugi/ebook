import africastalking
import os
from payments.sub_logger import logger


def query_transactions():
    logger.info("tasks.query_transactions: Starting Execution")

    africastalking_username = os.environ['AFRICASTALKING_USERNAME']
    africastalking_api_key = os.environ['AFRICASTALKING_API_KEY']

    # Initialize the SDK
    africastalking.initialize(africastalking_username, africastalking_api_key)
    payment = africastalking.Payment

    # Set the name of your Africa's Talking payment product
    africastalking_product_name = os.environ['AFRICASTALKING_PRODUCT_NAME']

    filters = {
        "category": "MobileC2B",
        "status": "Success",
    }

    response = None

    # Fetch the product transactions
    try:
        response = payment.product_transactions(africastalking_product_name, filters)
        logger.info("tasks.query_transactions: Response: {}".format(response['responses']))

        return response['responses']
    except Exception as e:
        logger.error("tasks.query_transactions: Received error response:%s" % str(e))


def validate_transaction(transaction_code):
    logger.info('tasks.validate_transaction: Start execution')

    successful_payment_status = False
    transactions = query_transactions()

    for payment in transactions:
        if payment['providerRefId'] == transaction_code:
            amount_paid = payment['value']  # payments['value'] is in string format

            """Change string to float. Example: 'KES 100.0' to 100.0"""
            amount_paid = float(amount_paid.lstrip('KES '))

            product_price = float(os.environ['PRODUCT_PRICE'])

            if amount_paid >= product_price:
                successful_payment_status = True

    return successful_payment_status
