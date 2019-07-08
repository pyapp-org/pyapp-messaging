import abc

from typing import Dict, Sequence, Any

__all__ = ("MessageSender", "MessageReceiver", "MessagePublisher", "MessageSubscriber")


class QueueBase(abc.ABC):
    """
    Base class of Message queues
    """

    __slots__ = ()

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
    def send(self, kwargs: Dict[str, Any]):
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
    def receive(self, count: int = 1) -> Sequence[Dict[str, Any]]:
        """
        Receive a message (or messages) from the task queue
        """

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
    def publish(self, kwargs: Dict[str, Any]):
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
    def subscribe(self, topic: str):
        """
        Subscribe to a named topic
        """

    @abc.abstractmethod
    def cancel_subscription(self, topic: str):
        """
        Unsubscribe from a topic
        """
