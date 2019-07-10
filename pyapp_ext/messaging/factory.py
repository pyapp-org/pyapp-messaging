from pyapp.conf.helpers import NamedPluginFactory, NoDefault

from .bases import MessageSender, MessageReceiver, MessagePublisher, MessageSubscriber

__all__ = (
    "message_sender_factory",
    "get_sender",
    "message_receiver_factory",
    "get_receiver",
    "message_publisher_factory",
    "get_publisher",
    "message_subscriber_factory",
    "get_subscriber",
)

message_sender_factory = NamedPluginFactory[MessageSender](
    "SEND_MESSAGE_QUEUES", abc=MessageSender, default_name=NoDefault
)
get_sender = message_sender_factory.create

message_receiver_factory = NamedPluginFactory[MessageReceiver](
    "RECEIVE_MESSAGE_QUEUES", abc=MessageReceiver, default_name=NoDefault
)
get_receiver = message_receiver_factory.create

message_publisher_factory = NamedPluginFactory[MessagePublisher](
    "PUBLISH_MESSAGE_QUEUES", abc=MessagePublisher, default_name=NoDefault
)
get_publisher = message_publisher_factory.create

message_subscriber_factory = NamedPluginFactory[MessageSubscriber](
    "SUBSCRIBE_MESSAGE_QUEUES", abc=MessageSubscriber, default_name=NoDefault
)
get_subscriber = message_subscriber_factory.create
