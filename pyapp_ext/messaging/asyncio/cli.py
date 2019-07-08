from asyncio import AbstractEventLoop
from pyapp.injection import inject
from typing import Any

from . import factory


@inject
def send(data: Any, config_name: str, *, loop: AbstractEventLoop):
    async def _send():
        async with factory.get_sender(config_name) as queue:
            await queue.send(data=data)

    loop.run_until_complete(_send())


@inject
def receiver(config_name: str, *, loop: AbstractEventLoop):
    async def _receiver():
        async with factory.get_receiver(config_name) as queue:
            await queue.listen()

    loop.run_until_complete(_receiver())


@inject
def publish(data: Any, config_name: str, *, loop: AbstractEventLoop):
    async def _send():
        async with factory.get_publisher(config_name) as queue:
            await queue.publish(data=data)

    loop.run_until_complete(_send())


@inject
def subscriber(config_name: str, *, loop: AbstractEventLoop):
    async def _receiver():
        async with factory.get_subscriber(config_name) as queue:
            await queue.listen()

    loop.run_until_complete(_receiver())
