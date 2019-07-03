"""
WSGI config for liyapilates project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
import os
from django.core.wsgi import get_wsgi_application
from whitenoise import DjangoWhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'liyapilates.settings')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bootcamp.settings")

application = get_wsgi_application()
application = DjangoWhiteNoise(application)
