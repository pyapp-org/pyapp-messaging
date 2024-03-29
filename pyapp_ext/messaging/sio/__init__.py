"""
pyApp - Synchronous Messaging
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Standard messaging interfaces for synchronous messaging clients.

"""
from .bases import MessageSender, MessageReceiver, Message


class Extension:
    """
    pyApp Synchronous Messaging
    """

    default_settings = "pyapp_ext.messaging.default_settings"
    checks = ".checks"

    @staticmethod
    def ready():
        from pyapp.injection import register_factory
        from . import factory

        register_factory(MessageSender, factory.get_sender)
        register_factory(MessageReceiver, factory.get_receiver)
