import abc

from typing import Dict, Sequence, Any

__all__ = (
    "MessageSender",
    "MessageReceiver",
    "MessagePublisher",
    "MessageSubscriber",
)


class QueueBase(abc.ABC):
    """
    Base class of Async Message queues
    """

    __slots__ = ()

    async def __aenter__(self):
        await self.open()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def open(self):
        """
        Open queue
        """

    async def close(self):
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
    async def send(self, kwargs: Dict[str, Any]):
        """
        Send a message to the task queue
        """


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

    @abc.abstractmethod
    async def listen(self):
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
    async def publish(self, kwargs: Dict[str, Any]):
        """
        Publish a message to queue
        """


class MessageSubscriber(QueueBase, metaclass=abc.ABCMeta):
    """
    Publish-Subscribe messaging subscriber.

    Messages are broadcast to all subscribed listeners eg::

                     |--> [Subscriber 1]
        [Publisher] -|--> [Subscriber 2]
                     |--> [Subscriber 3]

    """

    __slots__ = ()

    @abc.abstractmethod
    async def subscribe(self, topic: str):
        """
        Subscribe to a named topic
        """

    @abc.abstractmethod
    async def cancel_subscription(self, topic: str):
        """
        Unsubscribe from a topic
        """
