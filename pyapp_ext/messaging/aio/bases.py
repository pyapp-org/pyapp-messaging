"""
AsyncIO ABCs
~~~~~~~~~~~~

Standard messaging interfaces for asynchronous messaging clients.

These interfaces to be used with both Message Queue and Pub/Sub style queues.

"""
import abc
import logging
from typing import Any, AsyncGenerator, NamedTuple, Dict, Optional

from ..serialisation import Serialise, JSONSerialise

LOGGER = logging.getLogger(__name__)
DEFAULT_SERIALISE = JSONSerialise()


class QueueBase(abc.ABC):
    """
    Base class for Async Message queues
    """

    __slots__ = ()

    default_serialisation: Serialise = DEFAULT_SERIALISE

    def __repr__(self):
        return f"<{type(self).__name__}>"

    async def __aenter__(self):
        """
        Context manager enter
        """
        await self.open()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit
        """
        await self.close()

    @abc.abstractmethod
    async def open(self):
        """
        Open connection to queue
        """

    @abc.abstractmethod
    async def close(self):
        """
        Close connection to queue
        """

    @property
    def serialisation(self) -> Serialise:
        """
        Serialisation
        """
        return self.default_serialisation

    async def configure(self):
        """
        Configure/Create message queue
        """


class MessageSender(QueueBase, metaclass=abc.ABCMeta):
    """
    Message sender for either Message Queue or Pub/Sub style queues.
    """

    __slots__ = ()

    @abc.abstractmethod
    async def send_raw(
        self, body: str, *, content_type: str = None, content_encoding: str = None
    ):
        """
        Send a raw message to the task queue. This accepts a prepared and encoded body.
        """

    async def send(self, d: Dict[str, Any] = None, **data):
        """
        Send a message to the task queue.
        """
        if d:
            data.update(d)

        serialisation = self.serialisation
        await self.send_raw(
            serialisation.serialise(data),
            content_type=serialisation.content_type,
            content_encoding=serialisation.content_encoding,
        )


class Message(NamedTuple):
    """
    Message Received
    """

    body: Any
    content_type: str
    content_encoding: Optional[str]
    envelope: Any
    queue: "MessageReceiver"

    async def delete(self):
        """
        Delete this message
        """
        await self.queue.delete(self)

    @property
    def content(self):
        """
        De-serialised message content
        """
        return self.queue.serialisation.deserialise(self.body)


class MessageReceiver(QueueBase, metaclass=abc.ABCMeta):
    """
    Message receiver for either Messaging Queue or Pub/Sub style queues.
    """

    __slots__ = ()

    @abc.abstractmethod
    async def receive_raw(self) -> AsyncGenerator[Message, None]:
        """
        Receive a raw item from queue.
        """

    @abc.abstractmethod
    async def delete(self, message: Message):
        """
        Delete/Acknowledge message from queue
        """

    async def listen(
        self, *, auto_delete: bool = True
    ) -> AsyncGenerator[Message, None]:
        """
        Listen to queue for messages.
        """
        async for msg in self.receive_raw():
            yield msg
            if auto_delete:
                await self.delete(msg)
