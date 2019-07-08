import abc

from typing import Any

from .serialisation import Serialise, JSONSerialise

__all__ = ("MessageSender", "MessageReceiver", "MessagePublisher", "MessageSubscriber")


DEFAULT_SERIALISE = JSONSerialise()


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
    Message Queue messaging pattern sender.

    Messages are delivered to the first listening receiver
    eg::

                  |--> [Receiver 1]
        [Sender] -|    [Receiver 2]
                  |    [Receiver 2]

    """

    __slots__ = ()

    @abc.abstractmethod
    def send_raw(
        self, body: bytes, *, content_type: str = None, content_encoding: str = None
    ):
        """
        Send a raw message to the task queue. This accepts a prepared and encoded body.
        """

    def send(self, **kwargs: Any):
        """
        Send a message to the task queue.
        """
        serialisation = self.serialisation
        self.send_raw(
            serialisation.serialise(kwargs),
            content_type=serialisation.content_type,
            content_encoding=serialisation.content_encoding,
        )


class MessageReceiver(QueueBase, metaclass=abc.ABCMeta):
    """
    Message Queue messaging pattern receiver.

    Messages are delivered to the first listening receiver
    eg::

                  |--> [Receiver 1]
        [Sender] -|    [Receiver 2]
                  |    [Receiver 2]

    """

    __slots__ = ()

    def receive(
        self,
        message_body: bytes,
        content_type: str = None,
        content_encoding: str = None,
    ):
        """
        Called when a message is received.
        """
        body = self.serialisation.deserialise(message_body)
        print(content_type, content_encoding, body)

    @abc.abstractmethod
    def listen(self):
        """
        Start listening on the queue for messages
        """


class MessagePublisher(QueueBase, metaclass=abc.ABCMeta):
    """
    Publish-Subscribe messaging publisher.

    Messages are broadcast to all subscribed listeners eg::

                     |--> [Subscriber 1]
        [Publisher] -|--> [Subscriber 2]
                     |--> [Subscriber 3]

    """

    __slots__ = ()

    @abc.abstractmethod
    def publish_raw(
        self, body: bytes, *, content_type: str = None, content_encoding: str = None
    ):
        """
        Publish a raw message to queue. This accepts a prepared and encoded body.
        """

    def publish(self, **kwargs: Any):
        """
        Publish a message to queue
        """
        serialisation = self.serialisation
        self.publish_raw(
            serialisation.serialise(kwargs),
            content_type=serialisation.content_type,
            content_encoding=serialisation.content_encoding,
        )


class MessageSubscriber(QueueBase, metaclass=abc.ABCMeta):
    """
    Publish-Subscribe messaging subscriber.

    Messages are broadcast to all subscribed listeners eg::

                     |--> [Subscriber 1]
        [Publisher] -|--> [Subscriber 2]
                     |--> [Subscriber 3]

    """

    __slots__ = ()

    def receive(
        self,
        message_body: bytes,
        content_type: str = None,
        content_encoding: str = None,
    ):
        """
        Called when a message is received.
        """
        body = self.serialisation.deserialise(message_body)
        print(content_type, content_encoding, body)

    @abc.abstractmethod
    def subscribe(self, topic: str):
        """
        Subscribe to a named topic
        """
