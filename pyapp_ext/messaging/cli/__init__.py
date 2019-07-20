"""
pyApp - Messaging CLI

"""
import sys

from argparse import FileType
from pyapp.app import argument, CommandGroup, CommandOptions, KeyValueAction


class Extension:
    """
    pyApp Messaging
    """

    @staticmethod
    def register_commands(root: CommandGroup):
        group = root.create_command_group("msg-queue")

        @group.command
        @argument("NAME", help_text="Name of queue from config.")
        @argument("ARGS", nargs="+", action=KeyValueAction)
        def send(opts: CommandOptions):
            """
            Send a message to a Message Queue
            """
            from ..asyncio.cli import send

            send(opts.ARGS, opts.NAME)

        @group.command(name="send-raw")
        @argument("NAME", help_text="Name of queue from config.")
        @argument(
            "--body",
            type=FileType(),
            default=sys.stdin,
            help_text="Body of the message; defaults to stdin",
        )
        @argument("--content-type", help_text="Content type of raw data.")
        @argument("--content-encoding", help_text="Content encoding of raw data.")
        def send_raw(opts: CommandOptions):
            """
            Send a raw message directly from a file.
            """
            from ..asyncio.cli import send

            send(
                opts.body.read(),
                opts.NAME,
                raw=True,
                content_type=opts.content_type,
                content_encoding=opts.content_encoding,
            )

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
