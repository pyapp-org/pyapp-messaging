from pyapp.conf.helpers import NamedPluginFactory, NoDefault

from .bases import MessageSender, MessageReceiver

__all__ = (
    "message_sender_factory",
    "get_sender",
    "message_receiver_factory",
    "get_receiver",
)

message_sender_factory = NamedPluginFactory[MessageSender](
    "SEND_MESSAGE_QUEUES", abc=MessageSender, default_name=NoDefault
)
get_sender = message_sender_factory.create

message_receiver_factory = NamedPluginFactory[MessageReceiver](
    "RECEIVE_MESSAGE_QUEUES", abc=MessageReceiver, default_name=NoDefault
)
get_receiver = message_receiver_factory.create
