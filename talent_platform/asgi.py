"""
ASGI config for talent_platform project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from communications.consumers import NotificationsConsumer
from django.contrib.auth.middleware import AuthenticationMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'talent_platform.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': URLRouter([
        path('ws/notifications/', NotificationsConsumer.as_asgi()),
    ]),
})
