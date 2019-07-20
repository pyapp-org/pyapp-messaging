import logging
import sys

from asyncio import AbstractEventLoop
from colorama import Fore
from functools import partial
from pyapp.exceptions import NotFound, CannotImport
from pyapp.injection import inject
from typing import Any

from pyapp_ext.messaging.exceptions import QueueNotFound
from . import factory, Message

logger = logging.getLogger(__name__)


print_err = partial(print, file=sys.stderr)


@inject
def send(
    data: Any,
    config_name: str,
    *,
    raw: bool = False,
    content_type: str = None,
    content_encoding: str = None,
    loop: AbstractEventLoop,
):
    async def _send():
        try:
            async with factory.get_sender(config_name) as queue:
                if raw:
                    await queue.send_raw(
                        data,
                        content_type=content_type,
                        content_encoding=content_encoding,
                    )
                else:
                    await queue.send(**data)

        except (NotFound, CannotImport) as ex:
            print_err(str(ex))
            return -1

        except QueueNotFound:
            print_err(f"Queue not found.")
            return -2

        return 0

    return loop.run_until_complete(_send())


@inject
def receiver(config_name: str, *, loop: AbstractEventLoop):
    async def on_new_message(msg: Message):
        print(f"From {msg.queue} received: {msg.body}")

    try:
        queue = factory.get_receiver(config_name)
    except (NotFound, CannotImport) as ex:
        logger.error(str(ex))
        return -1

    queue.new_message.bind(on_new_message)

    logger.info("Starting listener...")
    try:
        loop.run_until_complete(queue.open())
        loop.run_forever()

    except QueueNotFound:
        logger.error("Queue not found.")
        return -2

    except (SystemExit, KeyboardInterrupt):
        return 0

    finally:
        logger.info("Stopping listener...")
        loop.run_until_complete(queue.close())

    return 0


@inject
def configure(*, loop: AbstractEventLoop):
    factories = [factory.message_sender_factory, factory.message_receiver_factory]

    async def _configure():
        for queue_factory in factories:
            print(f"Configuring queues in {type(queue_factory)}")
            for config_name in queue_factory.available:
                print(f"- {Fore.BLUE}{config_name:20s}{Fore.RESET}", end="")

                try:
                    instance = queue_factory.create(config_name)
                except CannotImport as ex:
                    print(f" {Fore.RED}[Critical]{Fore.RESET}: {ex}")
                else:
                    try:
                        await instance.configure()
                    except Exception as ex:
                        print(f" {Fore.RED}[Failed]{Fore.RESET}: {ex}")
                    else:
                        print(f" {Fore.GREEN}[OK]{Fore.RESET}")
            print()

        return 0

    return loop.run_until_complete(_configure())
