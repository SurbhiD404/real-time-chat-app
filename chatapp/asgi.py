"""
ASGI config for chatapp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatapp.settings')

import importlib

def get_websocket_application():
    import chat.routing
    return URLRouter(chat.routing.websocket_urlpatterns)

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': get_websocket_application(),
})