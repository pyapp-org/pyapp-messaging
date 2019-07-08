"""
pyApp - Async Messaging

"""
from .bases import *


class Extension:
    """
    pyApp - Async Messaging
    """

    default_settings = "pyapp_ext.messaging.default_settings"
    checks = ".checks"

    @staticmethod
    def ready():
        from pyapp.injection import register_factory
        from . import factory

        register_factory(MessageSender, factory.get_sender)
        register_factory(MessageReceiver, factory.get_receiver)
        register_factory(MessagePublisher, factory.get_publisher)
        register_factory(MessageSubscriber, factory.get_subscriber)
