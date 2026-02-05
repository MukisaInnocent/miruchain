"""
ASGI config for MIRUCHAIN project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'miruchain.settings')

application = get_asgi_application()
