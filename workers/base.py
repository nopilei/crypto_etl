from channels.consumer import SyncConsumer


class BaseWorker(SyncConsumer):

    async def run(self, event):
        raise NotImplementedError
