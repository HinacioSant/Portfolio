"""
WSGI config for Portfolio project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
import traceback
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Portfolio.settings')


try:
    # your Django application code here
    application = get_wsgi_application()

except Exception as e:
    traceback.print_exc()
