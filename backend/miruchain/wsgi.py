"""
WSGI config for MIRUCHAIN project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'miruchain.settings')

application = get_wsgi_application()
