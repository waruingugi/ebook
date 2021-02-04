from payments.models import Customers
from django.db.models.signals import post_save
from django.dispatch import receiver
from payments.sub_logger import logger
import requests
import os


@receiver([post_save], sender=Customers)
def send_message(sender, instance, **kwargs):
    logger.info('signals.send_message: Sending product to {}'.format(instance.email))

    customer_data = {
        'Name': instance.name,
        'email': instance.email
    }
    sendpulse_url = os.environ['SENDPULSE_URL']

    requests.post(sendpulse_url, data=customer_data)
