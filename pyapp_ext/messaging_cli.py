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
            from .messaging.asyncio.factory import get_sender

            async def _send():
                async with get_sender(opts.NAME) as queue:
                    await queue.send()

            loop.run_until_complete(_send())

        @group.command(help_text="Send a message to a Message Queue")
        @argument("NAME", help_text="Name of queue from config.")
        @inject
        def receiver(opts: CommandOptions, *, loop: AbstractEventLoop):
            from .messaging.asyncio.factory import get_receiver

            async def _receiver():
                async with get_receiver(opts.NAME) as queue:
                    await queue.listen()

            loop.run_until_complete(_receiver())

        @group.command(help_text="Send a message to a Pub/Sub Queue")
        @argument("NAME", help_text="Name of queue from config.")
        @argument("--body", type=FileType("r"))
        def publish(opts: CommandOptions):
            pass
