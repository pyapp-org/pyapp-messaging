import sys

from asyncio import AbstractEventLoop
from colorama import Fore
from pyapp.injection import inject
from typing import Any

from pyapp_ext.messaging.exceptions import QueueNotFound
from . import factory, Message


async def on_new_message(msg: Message):
    print(f"From {msg.queue} recieved: {msg.body}")


@inject
def send(data: Any, config_name: str, *, loop: AbstractEventLoop):
    async def _send():
        try:
            async with factory.get_sender(config_name) as queue:
                await queue.send(data=data)

        except QueueNotFound:
            print(f"Queue not found.", file=sys.stderr)
            return -1

        return 0

    return loop.run_until_complete(_send())


@inject
def receiver(config_name: str, *, loop: AbstractEventLoop):
    async def _receiver():
        try:
            async with factory.get_receiver(config_name) as queue:
                queue.new_message.bind(on_new_message)
                await queue.listen()

        except QueueNotFound:
            print(f"Queue not found.", file=sys.stderr)
            return -1

        return 0

    return loop.run_until_complete(_receiver())


@inject
def configure(*, loop: AbstractEventLoop):
    factories = [factory.message_sender_factory, factory.message_receiver_factory]

    async def _configure():
        for queue_factory in factories:
            print(f"Configuring queues in {type(queue_factory)}")
            for config_name in queue_factory.available:
                print(f"- {Fore.BLUE}{config_name:20s}{Fore.RESET}", end="")

                instance = queue_factory.create(config_name)
                try:
                    await instance.configure()
                except Exception as ex:
                    print(f" {Fore.RED}[Failed]{Fore.RESET}: {ex}")
                else:
                    print(f" {Fore.GREEN}[OK]{Fore.RESET}")
            print()

        return 0

    return loop.run_until_complete(_configure())
