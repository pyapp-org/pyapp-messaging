from pyapp.checks.registry import register

from .factory import (
    message_sender_factory,
    message_receiver_factory,
    message_publisher_factory,
    message_subscriber_factory,
)

register(message_sender_factory)
register(message_receiver_factory)
register(message_publisher_factory)
register(message_subscriber_factory)
