"""
Bases
~~~~~

Definitions of interface classes for interacting with Message Queues.

These interfaces to be used with both Message Queue and Pub/Sub style queues.

Both Sender and Receiver interfaces are also defined for AsyncIO in the
`asyncio` sub-package.


Message Queues
--------------

This pattern is used for task/job queues where a message is sent to the queue
and then delivered to one of the multiple listeners. This pattern commonly
utilises a timeout and retry mechanism to handle failures in the processing
of a message.

Visually the queue looks like::

                  |--> [Receiver 1]
        [Sender] -|    [Receiver 2]
                  |    [Receiver 2]


While this diagram greatly simplifies the role of the server between the sender
and receiver from your applications point of view that is outside the scope of
what pyApp Messaging provides.


Pub/Sub Queues
--------------

This pattern is used for notifications, event-bus queues where is sent to the
queue and then delivered to all listeners. This allows for events to be broadcast
to all subsystems without a larger application or for notification of events to
systems outside of your application.

Visually the queue looks like::

                     |--> [Subscriber 1]
        [Publisher] -|--> [Subscriber 2]
                     |--> [Subscriber 3]


Again this diagram greatly simplifies the role of the server. Typically messages
in a pub/sub queue are only available while your endpoint is connected. However,
if your applications requires that all events are processed a hybrid approach can
be utilised, see the next section.


Hybrid Queues
-------------

Another common pattern is for pub/sub messages be placed into a task queue for
certain subsystems that require all messages to be processed. A good example is
a system that reacts to certain events and can't miss events.

The configuration of this kind of queues is beyond the scope of pyApp-Messaging
and will depend entirely on the particular queuing server you are using.

Without supporting any particular messaging server, Rabbit MQ makes does allow
for fairly complex hybrid queuing models, while combination of AWS SQS and SNS
can be used to provide a basic hybrid setup.

"""
import abc

from typing import Any, Callable, Awaitable, NamedTuple
from pyapp import events

from .serialisation import Serialise, JSONSerialise

__all__ = ("MessageSender", "MessageReceiver", "Message")


DEFAULT_SERIALISE = JSONSerialise()


class Message(NamedTuple):
    """
    Message received
    """

    body: str
    content_type: str
    content_encoding: str
    queue: Any


class QueueBase(abc.ABC):
    """
    Base class of Async Message queues
    """

    __slots__ = ()

    serialisation: Serialise = DEFAULT_SERIALISE

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def open(self):
        """
        Open queue
        """

    def close(self):
        """
        Close Queue
        """


class MessageSender(QueueBase, metaclass=abc.ABCMeta):
    """
    Message sender for either Message Queue or Pub/Sub style queues.
    """

    __slots__ = ()

    @abc.abstractmethod
    def send_raw(
        self, body: bytes, *, content_type: str = None, content_encoding: str = None
    ) -> str:
        """
        Send a raw message to the task queue. This accepts a prepared and encoded body.
        """

    def send(self, **kwargs: Any) -> str:
        """
        Send a message to the task queue.
        """
        serialisation = self.serialisation
        return self.send_raw(
            serialisation.serialise(kwargs),
            content_type=serialisation.content_type,
            content_encoding=serialisation.content_encoding,
        )

    def configure(self):
        """
        Configure/Create message queue
        """


class MessageReceiver(QueueBase, metaclass=abc.ABCMeta):
    """
    Message receiver for either Messaging Queue or Pub/Sub style queues.
    """

    __slots__ = ()

    new_message = events.Callback[Callable[[Message], Awaitable]]()

    def receive(
        self,
        message_body: bytes,
        content_type: str = None,
        content_encoding: str = None,
    ):
        """
        Called when a message is received.
        """
        msg = Message(
            self.serialisation.deserialise(message_body),
            content_type,
            content_encoding,
            self,
        )
        self.new_message(msg)

    @abc.abstractmethod
    def listen(self):
        """
        Start listening on the queue for messages
        """

    def configure(self):
        """
        Configure/Create message queue
        """
