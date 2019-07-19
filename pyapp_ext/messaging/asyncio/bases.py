import abc

from typing import Any, Callable, Awaitable, NamedTuple
from pyapp import events

from ..serialisation import Serialise, JSONSerialise

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
    Message sender for either Message Queue or Pub/Sub style queues.
    """

    __slots__ = ()

    @abc.abstractmethod
    async def send_raw(
        self, body: bytes, *, content_type: str = None, content_encoding: str = None
    ) -> str:
        """
        Send a raw message to the task queue. This accepts a prepared and encoded body.
        """

    async def send(self, **kwargs: Any) -> str:
        """
        Send a message to the task queue.
        """
        serialisation = self.serialisation
        return await self.send_raw(
            serialisation.serialise(kwargs),
            content_type=serialisation.content_type,
            content_encoding=serialisation.content_encoding,
        )

    async def configure(self):
        """
        Configure/Create message queue
        """


class MessageReceiver(QueueBase, metaclass=abc.ABCMeta):
    """
    Message receiver for either Messaging Queue or Pub/Sub style queues.
    """

    __slots__ = ()

    new_message = events.AsyncCallback[Callable[[Message], Awaitable]]()

    async def receive(
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
        await self.new_message(msg)

    @abc.abstractmethod
    async def listen(self):
        """
        Start listening on the queue for messages
        """

    async def configure(self):
        """
        Configure/Create message queue
        """
