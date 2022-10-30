from apps.polygon.etl.base import BasePolygonWorkerWSConsumer


class PolygonQuotesWorkerConsumer(BasePolygonWorkerWSConsumer):
    REQUEST_PARAMS = [
        'XQ.BTC-USD',
        'XQ.ETH-USD',
        'XQ.ETH-BTC',
    ]
    GROUP_NAME = 'quotes'
