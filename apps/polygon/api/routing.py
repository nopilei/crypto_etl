from django.urls import re_path

from apps.polygon.api.all_quotes import PolygonAllQuotesConsumer
from apps.polygon.api.quotes import PolygonQuotesClientConsumer

urlpatterns = [
    re_path('quotes/all', PolygonAllQuotesConsumer.as_asgi()),
    re_path('quotes', PolygonQuotesClientConsumer.as_asgi()),
]
