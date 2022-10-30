import json
import logging
from urllib.parse import parse_qs

from apps.polygon.api.base import BasePolygonClientWSConsumer
from apps.polygon.api.const import AVAILABLE_QUOTE_PARAMS
from apps.polygon.etl.quotes import PolygonQuotesWorkerConsumer

logger = logging.getLogger(__name__)


class PolygonQuotesClientConsumer(BasePolygonClientWSConsumer):
    WRONG_PARAM_TEMPLATE = 'Pair {pair} is not in list: {list}'
    WORKER_CLASS = PolygonQuotesWorkerConsumer

    def __init__(self):
        self.pairs = []
        super().__init__()

    async def connect(self):
        await self.accept()

        url_params = parse_qs(self.scope['query_string'].decode())
        pairs = url_params.get('pairs')
        if pairs is not None:
            pairs = pairs[0].split(',')
        else:
            pairs = AVAILABLE_QUOTE_PARAMS[:]

        for pair in pairs:
            if pair not in AVAILABLE_QUOTE_PARAMS:
                message = self.WRONG_PARAM_TEMPLATE.format(pair=pair, list=AVAILABLE_QUOTE_PARAMS)
                await self.send(text_data=json.dumps({"message": message}), close=True)

        self.pairs = pairs
        await self.channel_layer.group_add(self.group_name, self.channel_name)

    def _transform_message(self, event) -> list:
        try:
            message = []
            pairs = json.loads(event['message'])
            for pair in pairs:
                pair_type = pair['pair']
                if pair_type in self.pairs:
                    group_message = {
                        'pair': pair_type,
                        'bid_price': pair['bp'],
                        'ask_price': pair['ap']
                    }
                    message.append(group_message)

            return message
        except Exception:
            logger.exception('ERROR')
