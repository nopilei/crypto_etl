import subprocess

from asgiref.sync import async_to_sync
from apps_config.const import channel_layer

async_to_sync(channel_layer.send)('polygon-quotes', {'type': 'run'})

subprocess.run(["python", "manage.py", "runworker", "polygon-quotes"])
