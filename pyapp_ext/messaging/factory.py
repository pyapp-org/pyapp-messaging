from pyapp.conf.helpers import NamedPluginFactory

from .bases import MessageQueue, PubSubQueue, AsyncMessageQueue, AsyncPubSubQueue

__all__ = (
    "message_queue_factory", "get_message_queue",
    "async_message_queue_factory", "async_get_message_queue",
    "pub_sub_queue_factory", "get_pub_sub_queue",
    "async_pub_sub_queue_factory", "async_get_pub_sub_queue",
)

message_queue_factory = NamedPluginFactory[MessageQueue](
    "MESSAGE_QUEUES", abc=MessageQueue
)
get_message_queue = message_queue_factory.create

async_message_queue_factory = NamedPluginFactory[AsyncMessageQueue](
    "MESSAGE_QUEUES", abc=AsyncMessageQueue
)
async_get_message_queue = async_message_queue_factory.create

pub_sub_queue_factory = NamedPluginFactory[PubSubQueue](
    "PUB_SUB_QUEUES", abc=PubSubQueue
)
get_pub_sub_queue = pub_sub_queue_factory.create

async_pub_sub_queue_factory = NamedPluginFactory[AsyncPubSubQueue](
    "PUB_SUB_QUEUES", abc=AsyncPubSubQueue
)
async_get_pub_sub_queue = async_pub_sub_queue_factory.create
