from pyapp.checks.registry import register

from .factory import (
    message_queue_factory,
    pubsub_queue_factory,
    async_message_queue_factory,
    async_pubsub_queue_factory,
)

register(message_queue_factory)
register(pubsub_queue_factory)
register(async_message_queue_factory)
register(async_pubsub_queue_factory)
