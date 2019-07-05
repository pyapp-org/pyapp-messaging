from pyapp.checks.registry import register

from .factory import (
    message_queue_factory,
    pub_sub_queue_factory,
    async_message_queue_factory,
    async_pub_sub_queue_factory,
)

register(message_queue_factory)
register(pub_sub_queue_factory)
register(async_message_queue_factory)
register(async_pub_sub_queue_factory)
