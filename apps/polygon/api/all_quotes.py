import json

from channels.generic.websocket import AsyncWebsocketConsumer

from apps.polygon.api.const import AVAILABLE_QUOTE_PARAMS


class PolygonAllQuotesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps(AVAILABLE_QUOTE_PARAMS), close=True)
