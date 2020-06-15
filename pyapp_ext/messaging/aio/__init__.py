"""
pyApp - AsyncIO Messaging
~~~~~~~~~~~~~~~~~~~~~~~~~

Standard messaging interfaces for Asyncio based messaging clients.

For common platforms install the associated client:

- AWS SQS/SNS - pyapp.aiobotocore

- AMQP/RabbitMQ - pyapp.aiopika

"""
from .bases import MessageSender, MessageReceiver, Message


class Extension:
    """
    pyApp - AsyncIO Messaging
    """

    default_settings = "pyapp_ext.messaging.default_settings"
    checks = ".checks"

    @staticmethod
    def ready():
        from pyapp.injection import register_factory
        from . import factory

        register_factory(MessageSender, factory.get_sender)
        register_factory(MessageReceiver, factory.get_receiver)
