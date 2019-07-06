import abc

from pyapp.events import AsyncEvent, Event
from typing import Sequence, Callable, Awaitable, Dict

__all__ = ("MessageQueue", "PubSubQueue", "AsyncMessageQueue", "AsyncPubSubQueue")


class QueueBase(abc.ABC):
    """
    Base class for Message queues
    """

    def __enter__(self) -> None:
        self.open()

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


class MessageQueue(QueueBase, metaclass=abc.ABCMeta):
    """
    Message Queue messaging pattern.

    Messages are delivered to the first listener to query for the next message
    eg::

                  |--> [Listener 1]
        [Sender] -|    [Listener 2]
                  |    [Listener 2]

    """

    new_message = Event[Callable[[str], None]]()

    @abc.abstractmethod
    def send(self, kwargs: Dict[str, str]):
        """
        Send a message to the task queue
        """

    @abc.abstractmethod
    def receive(self, count: int = 1) -> Sequence[str]:
        """
        Receive a message (or messages) from the task queue
        """

    @abc.abstractmethod
    def listen(self):
        """
        Start listening on the queue for messages
        """


class PubSubQueue(QueueBase, metaclass=abc.ABCMeta):
    """
    Publish-Subscribe messaging pattern.

    Messages are broadcast to all subscribed listeners eg::

                  |--> [Listener 1]
        [Sender] -|--> [Listener 2]
                  |--> [Listener 3]

    """

    @abc.abstractmethod
    def publish(self, kwargs: Dict[str, str], topic: str):
        """
        Publish a message to queue
        """

    @abc.abstractmethod
    def subscribe(self, topic: str):
        """
        Subscribe to a named topic
        """

    @abc.abstractmethod
    def cancel_subscription(self, topic: str):
        """
        Unsubscribe from a topic
        """


class AsyncQueueBase(abc.ABC):
    """
    Base class of Async Message queues
    """

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


class AsyncMessageQueue(AsyncQueueBase, metaclass=abc.ABCMeta):
    """
    Message Queue messaging pattern.

    Messages are delivered to the first listener to query for the next message
    eg::

                  |--> [Listener 1]
        [Sender] -|    [Listener 2]
                  |    [Listener 2]

    """

    new_message = AsyncEvent[Callable[[str], Awaitable]]()

    @abc.abstractmethod
    async def send(self, kwargs: Dict[str, str]):
        """
        Send a message to the task queue
        """

    @abc.abstractmethod
    async def receive(self, count: int = 1) -> Sequence[str]:
        """
        Receive a message (or messages) from the task queue
        """

    @abc.abstractmethod
    async def listen(self):
        """
        Start listening on the queue for messages
        """


class AsyncPubSubQueue(AsyncQueueBase, metaclass=abc.ABCMeta):
    """
    Publish-Subscribe messaging pattern.

    Messages are broadcast to all subscribed listeners eg::

                  |--> [Listener 1]
        [Sender] -|--> [Listener 2]
                  |--> [Listener 3]

    """

    @abc.abstractmethod
    async def publish(self, kwargs: Dict[str, str]):
        """
        Publish a message to queue
        """

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
