"""
pyApp - Messaging CLI

"""
from asyncio import AbstractEventLoop
from argparse import FileType

from pyapp.app import argument, CommandGroup, CommandOptions
from pyapp.injection import inject


class Extension:
    """
    pyApp Messaging
    """

    @staticmethod
    def register_commands(root: CommandGroup):
        group = root.create_command_group("msg-queue")

        @group.command(help_text="Send a message to a Message Queue")
        @argument("NAME", help_text="Name of queue from config.")
        @argument("--body", type=FileType("r"))
        @inject
        def send(opts: CommandOptions, *, loop: AbstractEventLoop):
            from .messaging.factory import async_get_message_queue

            async def _send():
                async with async_get_message_queue(opts.NAME) as queue:
                    await queue.send()

            loop.run_until_complete(_send())

        @group.command(help_text="Send a message to a Pub/Sub Queue")
        @argument("NAME", help_text="Name of queue from config.")
        @argument("--body", type=FileType("r"))
        def publish(opts: CommandOptions):
            pass
