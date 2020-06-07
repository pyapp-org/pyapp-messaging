"""
Synchronous ABCs
~~~~~~~~~~~~~~~~

Standard messaging interfaces for synchronous messaging clients.

These interfaces to be used with both Message Queue and Pub/Sub style queues.

"""
import abc
import logging
from typing import Any, Generator, NamedTuple

from ..serialisation import Serialise, JSONSerialise

LOGGER = logging.getLogger(__name__)
DEFAULT_SERIALISE = JSONSerialise()


class QueueBase(abc.ABC):
    """
    Base class of Synchronous Message queues
    """

    __slots__ = ()

    default_serialisation: Serialise = DEFAULT_SERIALISE

    def __repr__(self):
        return f"<{type(self).__name__}>"

    def __enter__(self):
        """
        Context manager enter
        """
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit
        """
        self.close()

    @abc.abstractmethod
    def open(self):
        """
        Open connection to queue
        """

    @abc.abstractmethod
    def close(self):
        """
        Close connection to queue
        """

    @property
    def serialisation(self) -> Serialise:
        """
        Serialisation
        """
        return self.default_serialisation

    def configure(self):
        """
        Configure/Create message queue
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


class Message(NamedTuple):
    """
    Message Received
    """

    body: Any
    content_type: str
    content_encoding: str
    raw: Any
    queue: "MessageReceiver"

    def delete(self):
        """
        Delete this message
        """
        self.queue.delete(self)

    @property
    def content(self):
        """
        Deserialised message content
        """
        return self.queue.serialisation.deserialise(self.body)


class MessageReceiver(QueueBase, metaclass=abc.ABCMeta):
    """
    Message receiver for either Messaging Queue or Pub/Sub style queues.
    """

    __slots__ = ()

    @abc.abstractmethod
    def receive_raw(self) -> Generator[Message, None, None]:
        """
        Receive a raw item from queue.
        """

    @abc.abstractmethod
    def delete(self, message: Message):
        """
        Delete/Acknowledge message from queue
        """

    def listen(self, *, auto_delete: bool = True) -> Generator[Message, None, None]:
        """
        Listen to queue for messages.
        """
        while True:
            for msg in self.receive_raw():
                try:
                    yield msg
                    if auto_delete:
                        self.delete(msg)

                except ValueError as ex:
                    LOGGER.error("Bad message: unable to de-serialise message: %r", ex)

                except Exception:
                    LOGGER.exception("Un-handling error de-serialising message")