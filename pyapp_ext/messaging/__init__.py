"""
pyApp - Messaging

"""
from .bases import *


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

        register_factory(MessageQueue, factory.message_queue_factory.create)
        register_factory(PubSubQueue, factory.pub_sub_queue_factory.create)
        register_factory(AsyncMessageQueue, factory.async_message_queue_factory.create)
        register_factory(AsyncPubSubQueue, factory.async_pub_sub_queue_factory.create)
