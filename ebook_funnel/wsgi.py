"""
WSGI config for ebook_funnel project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os  # noqa

from django.core.wsgi import get_wsgi_application  # noqa
from dj_static import Cling  # noqa


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ebook_funnel.settings')

application = Cling(get_wsgi_application())
