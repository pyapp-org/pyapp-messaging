"""
pyApp - Messaging CLI

"""
import sys

from argparse import FileType
from pyapp.app import argument, CommandGroup, CommandOptions


class Extension:
    """
    pyApp Messaging
    """

    @staticmethod
    def register_commands(root: CommandGroup):
        group = root.create_command_group("msg-queue")

        @group.command
        @argument("NAME", help_text="Name of queue from config.")
        @argument(
            "--body",
            type=FileType("r"),
            default=sys.stdin,
            help_text="Body of the message; defaults to stdin",
        )
        def send(opts: CommandOptions):
            """
            Send a message to a Message Queue
            """
            from ..asyncio.cli import send

            send(opts.body.read(), opts.NAME)

        @group.command
        @argument("NAME", help_text="Name of queue from config.")
        def receiver(opts: CommandOptions):
            """
            Send a message to a Message Queue
            """
            from ..asyncio.cli import receiver

            receiver(opts.NAME)

        @group.command
        def configure(_: CommandOptions):
            """
            Configure/Create queues (if possible)
            """
            from ..asyncio.cli import configure

            configure()
