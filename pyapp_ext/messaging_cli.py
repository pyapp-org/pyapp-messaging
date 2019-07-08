"""
pyApp - Messaging CLI

"""
from argparse import FileType

from pyapp.app import argument, CommandGroup, CommandOptions


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
        def send(opts: CommandOptions):
            from .messaging.asyncio.cli import send

            send(opts.body.read(), opts.NAME)

        @group.command(help_text="Send a message to a Message Queue")
        @argument("NAME", help_text="Name of queue from config.")
        def receiver(opts: CommandOptions):
            from .messaging.asyncio.cli import receiver

            receiver(opts.NAME)

        @group.command(help_text="Send a message to a Pub/Sub Queue")
        @argument("NAME", help_text="Name of queue from config.")
        @argument("--body", type=FileType("r"))
        def publish(opts: CommandOptions):
            from .messaging.asyncio.cli import publish

            publish(opts.body.read(), opts.NAME)

        @group.command(help_text="Send a message to a Message Queue")
        @argument("NAME", help_text="Name of queue from config.")
        def subscriber(opts: CommandOptions):
            from .messaging.asyncio.cli import subscriber

            subscriber(opts.NAME)
