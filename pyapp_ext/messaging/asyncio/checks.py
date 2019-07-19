from pyapp.checks.registry import register

from .factory import message_sender_factory, message_receiver_factory

register(message_sender_factory)
register(message_receiver_factory)
