from typing import Type

from channels.generic.websocket import AsyncWebsocketConsumer

from apps.polygon.etl.base import BasePolygonWorkerWSConsumer


class BasePolygonClientWSConsumer(AsyncWebsocketConsumer):
    WORKER_CLASS: Type[BasePolygonWorkerWSConsumer]

    def __init__(self):
        self.group_name = self.WORKER_CLASS.GROUP_NAME
        super().__init__()

    def _transform_message(self, event) -> list:
        raise NotImplementedError

    async def from_polygon(self, event):
        """Process message from worker and send it to client"""

        message = self._transform_message(event)
        if message:
            await self.send(text_data=str(message))
