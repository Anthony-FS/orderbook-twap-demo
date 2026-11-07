"""ASGI entry point: the one object the server (daphne) runs.

ProtocolTypeRouter sends each incoming connection to the right handler:
plain HTTP requests go to normal Django views, WebSocket connections go to
Channels consumers. WebSocket routes are added in step 3 (/ws/market/) and
step 6 (/ws/orders/).
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Must be created before importing anything that touches Django models.
django_http_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter  # noqa: E402

websocket_urlpatterns: list = []

application = ProtocolTypeRouter(
    {
        "http": django_http_app,
        "websocket": URLRouter(websocket_urlpatterns),
    }
)
