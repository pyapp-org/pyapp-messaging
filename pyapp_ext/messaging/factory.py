from pyapp.conf.helpers import NamedPluginFactory

from .bases import MessageQueue, PubSubQueue, AsyncMessageQueue, AsyncPubSubQueue

__all__ = (
    "message_queue_factory",
    "pub_sub_queue_factory",
    "async_message_queue_factory",
    "async_pub_sub_queue_factory",
)


message_queue_factory = NamedPluginFactory[MessageQueue](
    "MESSAGE_QUEUES", abc=MessageQueue
)
pub_sub_queue_factory = NamedPluginFactory[PubSubQueue](
    "PUB_SUB_QUEUES", abc=PubSubQueue
)

async_message_queue_factory = NamedPluginFactory[AsyncMessageQueue](
    "MESSAGE_QUEUES", abc=AsyncMessageQueue
)
async_pub_sub_queue_factory = NamedPluginFactory[AsyncPubSubQueue](
    "PUB_SUB_QUEUES", abc=AsyncPubSubQueue
)
