from pyapp.conf.helpers import NamedPluginFactory

from .bases import MessageQueue, PubSubQueue, AsyncMessageQueue, AsyncPubSubQueue

__all__ = (
    "message_queue_factory",
    "pubsub_queue_factory",
    "async_message_queue_factory",
    "async_pubsub_queue_factory",
)


message_queue_factory = NamedPluginFactory[MessageQueue](
    "MESSAGE_QUEUES", abc=MessageQueue
)
pubsub_queue_factory = NamedPluginFactory[PubSubQueue]("PUBSUB_QUEUES", abc=PubSubQueue)

async_message_queue_factory = NamedPluginFactory[AsyncMessageQueue](
    "MESSAGE_QUEUES", abc=AsyncMessageQueue
)
async_pubsub_queue_factory = NamedPluginFactory[AsyncPubSubQueue](
    "PUBSUB_QUEUES", abc=AsyncPubSubQueue
)
