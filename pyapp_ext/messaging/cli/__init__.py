"""
pyApp - Messaging CLI
~~~~~~~~~~~~~~~~~~~~~

Provides a CLI extension for test sending messages

"""
import logging
import sys
from argparse import FileType
from pprint import pprint

from colorama import Fore
from pyapp.app import argument, CommandGroup, CommandOptions, KeyValueAction
from pyapp.exceptions import NotFound, CannotImport

from pyapp_ext.messaging.aio import factory
from ..exceptions import QueueNotFound

LOGGER = logging.getLogger(__name__)


class Extension:
    """
    pyApp Messaging
    """

    @staticmethod
    @argument("NAME", help_text="Name of queue from config.")
    @argument("ARGS", nargs="+", action=KeyValueAction)
    async def send(opts: CommandOptions):
        """
        Send a message to a Message Queue
        """
        try:
            async with factory.get_sender(opts.NAME) as queue:
                await queue.send(**opts.ARGS)

        except (NotFound, CannotImport) as ex:
            LOGGER.error(str(ex))
            return 10

        except QueueNotFound:
            LOGGER.error(f"Queue not found {opts.NAME!r}")
            return 20

        return 0

    @staticmethod
    @argument("NAME", help_text="Name of queue from config.")
    @argument(
        "--body",
        type=FileType(),
        default=sys.stdin,
        help_text="Body of the message; defaults to stdin",
    )
    @argument("--content-type", help_text="Content type of raw data.")
    @argument("--content-encoding", help_text="Content encoding of raw data.")
    async def send_raw(opts: CommandOptions):
        """
        Send a raw message directly from a file.
        """
        try:
            async with factory.get_sender(opts.NAME) as queue:
                await queue.send_raw(
                    opts.body.read(),
                    content_type=opts.content_type,
                    content_encoding=opts.content_encoding,
                )

        except (NotFound, CannotImport) as ex:
            LOGGER.error(str(ex))
            return 10

        except QueueNotFound:
            LOGGER.error(f"Queue not found {opts.NAME!r}")
            return 20

        return 0

    @staticmethod
    @argument("NAME", help_text="Name of queue from config.")
    @argument(
        "--out",
        type=FileType(),
        default=sys.stdout,
        help_text="Body of the message; defaults to stdin",
    )
    async def listen(opts: CommandOptions):
        """
        Receive and echo messages from an event queue.
        """
        try:
            queue = factory.get_receiver(opts.NAME)
        except (NotFound, CannotImport) as ex:
            LOGGER.error(str(ex))
            return 10

        LOGGER.info("Starting listener %r...", opts.NAME)
        try:
            async with queue:
                async for msg in queue.listen():
                    print(f"\n----\nFrom: {msg.queue!r}\nContent:", file=opts.out)
                    pprint(msg.content, stream=opts.out)

        except QueueNotFound:
            LOGGER.error("Queue not found.")
            return 20

        except (SystemExit, KeyboardInterrupt):
            pass

        finally:
            LOGGER.info("Stopping listener...")

        return 0

    @staticmethod
    async def configure(_opts: CommandOptions):
        """
        Configure/Create queues (if possible)
        """
        factories = [factory.message_sender_factory, factory.message_receiver_factory]

        for queue_factory in factories:
            print(f"Configuring queues in {queue_factory.setting}")
            for config_name in queue_factory.available:
                print(f" - {Fore.BLUE}{config_name:20s}{Fore.RESET}", end="")

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

    @staticmethod
    def queues(_opts: CommandOptions):
        """
        List all available queues
        """
        factories = [factory.message_sender_factory, factory.message_receiver_factory]

        for queue_factory in factories:
            print(queue_factory.setting)
            for name, (type_name, _) in queue_factory._instance_definitions.items():
                print(
                    f" - {Fore.BLUE}{name:20s}{Fore.RESET}"
                    f"{Fore.CYAN}{type_name}{Fore.RESET}"
                )
            print()

    @staticmethod
    def register_commands(root: CommandGroup):
        group = root.create_command_group("messaging")
        group.command(Extension.send)
        group.command(Extension.send_raw, name="send-raw")
        group.command(Extension.listen)
        group.command(Extension.configure)
        group.command(Extension.queues)
