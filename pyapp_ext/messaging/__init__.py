"""
pyApp - Messaging
~~~~~~~~~~~~~~~~~

A simple messaging interface covering Message Queue and Pub/Sub style queues
for distributed applications.

Provides three extensions Messaging, Messaging-Async and Messaging-CLI.

Messaging itself does not provide connectivity to messaging services, instead
implementation specific extensions provide client libraries that implement the
queue interfaces.

"""
from .__version__ import __version__
from .bases import *

version_info = (int(v) for v in __version__.split("."))


class Extension:
    """
    pyApp Messaging
    """

    default_settings = ".default_settings"
    checks = ".checks"

    @staticmethod
    def ready():
        from pyapp.injection import register_factory
        from . import factory

        register_factory(MessageSender, factory.get_sender)
        register_factory(MessageReceiver, factory.get_receiver)
