import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import ledapp.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ledproject.settings')

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(ledapp.routing.websocket_urlpatterns)
    ),
})
