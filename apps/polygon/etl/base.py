import json
import logging
import os

import websocket
from asgiref.sync import async_to_sync

from apps_config.const import channel_layer
from apps.polygon.etl.exceptions import ConnectionFailed, AuthenticationFailed, BadSubscriptionStatus
from workers.base import BaseWorker

logger = logging.getLogger(__name__)


class BasePolygonWorkerWSConsumer(BaseWorker):
    """
    Base worker task consumer for connecting to Polygon ws endpoints and sending data from it to channels groups
    """
    POLYGON_URL: str = os.environ['POLYGON_URL']
    AUTHENTICATION_KEY: str = os.environ['POLYGON_AUTHENTICATION_KEY']
    GROUP_NAME: str
    REQUEST_PARAMS: tuple[str]  # Vary on endpoints

    def start_broadcasting(self, connection: websocket.WebSocket) -> None:
        while True:
            message = connection.recv()

            # Deliver message processing to client to reduce excessive latency effect
            async_to_sync(channel_layer.group_send)(self.GROUP_NAME, {'type': 'from_polygon', 'message': message})

    def connect(self, connection: websocket.WebSocket) -> None:
        logger.info(f'Connecting to {self.POLYGON_URL}')

        connection.connect(self.POLYGON_URL)
        status = json.loads(connection.recv())[0]['status']
        if status != 'connected':
            raise ConnectionFailed(f'Got connection status: {status}. Message: {status}')

        logger.info('Connected successfully')

    def subscribe(self, connection: websocket.WebSocket) -> None:
        logger.info('Start subscription')

        connection.send(json.dumps({'action': 'subscribe', 'params': ','.join(self.REQUEST_PARAMS)}))
        message = json.loads(connection.recv())[0]
        while 'status' in message:
            status = message['status']
            if status != 'success':
                raise BadSubscriptionStatus(f'Bad subscription status: {status}')
            message = json.loads(connection.recv())[0]

        logger.info('Subscribed to all streams')

    def authenticate(self, connection: websocket.WebSocket) -> None:
        logger.info('Authentication')

        connection.send(json.dumps({'action': 'auth', 'params': self.AUTHENTICATION_KEY}))
        status = json.loads(connection.recv())[0]['status']
        if status != 'auth_success':
            raise AuthenticationFailed(f'Authentication failed with key "{self.AUTHENTICATION_KEY}"')

        logger.info('Authenticated successfully')

    def run(self, event):
        try:
            connection = websocket.WebSocket()

            self.connect(connection)
            self.authenticate(connection)
            self.subscribe(connection)
            self.start_broadcasting(connection)
        except Exception:
            logger.exception('ERROR')
        finally:
            logger.warning('Closing connection')
