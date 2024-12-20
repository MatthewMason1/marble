"""
WSGI config for marble project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Point to the settings module inside the marble subfolder
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "marble.marble.settings")

application = get_wsgi_application()