from channels.routing import ProtocolTypeRouter, ChannelNameRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path

from apps.polygon.etl.quotes import PolygonQuotesWorkerConsumer
from apps.polygon.api.routing import urlpatterns as polygon_urlpatterns

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "channel": ChannelNameRouter({
        "polygon-quotes": PolygonQuotesWorkerConsumer.as_asgi(),
    }),
    "websocket": URLRouter([
        path('ws/polygon/', URLRouter(
            polygon_urlpatterns
        )),
    ]),
})
